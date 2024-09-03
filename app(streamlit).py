import streamlit as st
import nest_asyncio
import os
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
index_storage_dir = "./index_store_dev/vector"

if 'index_store_dev' not in os.listdir():
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

# Streamlit app
st.title("Tamil Nadu Scheme Connect")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is up?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get response from the query engine
    with st.chat_message("assistant"):
        response=agent.chat(f'All details regarding the query asked in tamil nadu only and answer only what is asked no need to requestion ur own self, dont respond anything that is not from the documents. the query is : {prompt}')
        retriever = TavilySearchAPIRetriever(k=3)

        result=retriever.invoke(f'only from official goverment website of tamil nadu for the query:{prompt}')
        source=[document.metadata['source'] for document in result]
        for s in source:
            st.markdown(s)

        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
