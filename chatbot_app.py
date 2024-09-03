from flask import Flask, request, jsonify, render_template, redirect, url_for, session
import nest_asyncio
import os
import requests
from langchain_community.retrievers import TavilySearchAPIRetriever
from dotenv import load_dotenv
from llama_index.core import Settings, StorageContext, load_index_from_storage
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.agent.openai import OpenAIAgent

# Apply nested asyncio
nest_asyncio.apply()

# Load environment variables
load_dotenv()

# Configure Settings
Settings.llm = Groq(model="llama3-70b-8192")
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Directory for index storage
index_storage_dir = "./index_store_final/vector"

if 'index_store_final' not in os.listdir():
    # Load documents
    documents = SimpleDirectoryReader("./hack4", recursive=True).load_data()

    # Chunk documents
    splitter = SentenceSplitter(chunk_size=1024)
    nodes = splitter.get_nodes_from_documents(documents)

    # Create vector store index
    vector_index = VectorStoreIndex(nodes)

    # Persist the index
    os.makedirs(index_storage_dir, exist_ok=True)
    vector_index.storage_context.persist(persist_dir=index_storage_dir)
else:
    # Rebuild storage context and load index
    vector_storage_context = StorageContext.from_defaults(persist_dir=index_storage_dir)
    vector_index = load_index_from_storage(vector_storage_context)

# Create query engine tool
vector_query_engine = vector_index.as_query_engine()
query_engine_tools = [
    QueryEngineTool(
        query_engine=vector_query_engine,
        metadata=ToolMetadata(
            name="Tamil Nadu query engine",
            description=(
                "Provides information about Tamil Nadu's services in great detail and mentions all the schemes etc available for the user. "
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    )
]

# Initialize the agent
agent = OpenAIAgent.from_tools(query_engine_tools, verbose=True)

# Initialize Flask app
app = Flask(__name__, template_folder='templates')
app.secret_key = 'your_secret_key_here'  # Required for session management

# Home route
@app.route('/')
def home():
    if 'logged_in' in session:
        return render_template('index.html')
    return redirect(url_for('login'))

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Dummy check for demonstration purposes
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            return redirect(url_for('home'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

# Logout route
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/news')
def news():
    return render_template('newsmain.html')

# Chatbot Page Route
@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

# Map Page Route
@app.route('/map')
def map_page():
    return render_template('map.html')



# Chat API route
@app.route('/chat', methods=['POST'])
def chat():
    prompt = request.json.get("message")
    
    # Fetch the response from the agent
    agent_response = agent.chat(
        f'All details regarding the query asked in Tamil Nadu only and answer only what is asked; no need to re-question yourself. '
        f'Don’t respond with anything that is not from the documents. The query is: {prompt}'
    )
    
    # Convert agent_response to JSON-serializable format
    response_text = agent_response["text"] if isinstance(agent_response, dict) else str(agent_response)
    
    # Use the retriever to get sources
    retriever = TavilySearchAPIRetriever(k=3)
    result = retriever.invoke(f'only from official government website of Tamil Nadu for the query: {prompt}')
    
    # Extract sources, ensuring it's a list of strings
    sources = [document.metadata.get('source', '') for document in result]
    
    # Return the JSON response
    return jsonify({"response": response_text, "sources": sources})

# Whisper API settings
WHISPER_API_URL = 'https://api.openai.com/v1/audio/transcriptions'
WHISPER_API_KEY = 'your_whisper_api_key_here'

@app.route('/transcribe', methods=['POST'])
def transcribe():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']

    # Ensure the file is valid
    if not audio_file or audio_file.filename == '':
        return jsonify({'error': 'No audio file provided'}), 400

    # Prepare the request to the Whisper API
    headers = {
        'Authorization': f'Bearer {WHISPER_API_KEY}',
        'Content-Type': 'multipart/form-data'
    }
    files = {
        'file': (audio_file.filename, audio_file, 'audio/mpeg')
    }
    data = {
        'model': 'whisper-1',
        'language': 'en'
    }

    try:
        response = requests.post(WHISPER_API_URL, headers=headers, files=files, data=data)
        response.raise_for_status()  # Raise an error for HTTP errors

        # Parse the JSON response
        result = response.json()
        transcription = result.get('text', '')

        return jsonify({'transcription': transcription})
    
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)