# Tamil Nadu Scheme Connect

**Tamil Nadu Scheme Connect** is a web application designed to provide comprehensive information about government services and schemes available in Tamil Nadu. The app leverages advanced document indexing, language translation, and query processing technologies to deliver precise and relevant responses to user queries. 

## Overview

Built using Flask, JavaScript, CSS, and HTML, Tamil Nadu Scheme Connect offers users detailed insights into Tamil Nadu's government schemes and services. It integrates document indexing, language support, and a chat interface for efficient data retrieval and user interaction.

## Features

- **Document Indexing**: Efficiently indexes documents for quick search and retrieval using a vector database.
- **Query Handling**: Processes user inquiries to extract pertinent information from the indexed documents.
- **Language Translation**: Provides support for Tamil, Hindi, and English to accommodate a diverse audience.
- **Google API Integration**: Helps users locate nearby NGOs, hospitals, and blood donation camps.
- **News API Integration**: Retrieves and displays news related to legal issues, women's empowerment, and welfare.
- **Voice Input**: Allows users to interact with the chatbot using voice commands.

## How It Works

1. **Document Indexing**:
   - Loads and indexes documents from the `./hack4` directory.
   - Utilizes a sentence splitter to create nodes and stores the vector index in `./index_store_final/vector` for future use.

2. **Query Processing**:
   - User queries are processed by OpenAIAgent, leveraging a vector query engine to deliver detailed responses.
   - Retrieves additional information from Tamil Nadu government websites through TavilySearchAPIRetriever.

3. **Google API Integration**:
   - Finds nearby NGOs, hospitals, and blood donation camps based on user input.

4. **NewsAPI Integration**:
   - Fetches and shows news articles related to legal topics, women's empowerment, and welfare.

5. **Language Translation**:
   - Supports Tamil, Hindi, and English, allowing seamless language switching.

6. **Voice Input**:
   - Provides an interactive experience through voice command functionality.

## File Structure

- `chatbot_app.py`: Main Flask application file.
- `app.py`: Main Streamlit application file.
- `./hack4/`: Directory with PDF documents for indexing (not included here due to proprietary reasons).
- `./index_store_final/`: Directory for storing vector indexes (`vector.zip` available in the Google Drive link).
- `venv/`: (Optional) Environment variables file.
- `requirements.txt`: Lists the project dependencies.
- `Templates/`: Contains HTML files (`chatbot.html`, `index.html`, `login.html`, `map.html`, `newsmain.html`).
- `Scripts/`: Contains JavaScript and CSS files (`mapscripts.js`, `mapstyles.css`, `newsscripts.js`, `newsstyles.css`, `scripts.js`, `styles.css`).

## Dependencies

- **Flask**: For backend development of the web application.
- **JavaScript, CSS, HTML**: For frontend development.
- **Google API**: For locating nearby NGOs, hospitals, and blood donation camps.
- **News API**: For retrieving news articles.
- **langchain_community**: For API retrieval and document processing.
- **llama_index**: For document indexing and query processing.
- **dotenv**: For managing environment variables.

## Additional Resources

For convenience, you can download the indexed documents from the following Google Drive link: [Indexed Documents](https://drive.google.com/drive/folders/1X5AOffQVnzLr7H-8lfTrlOQuKWxrTcjT?usp=sharing)

## Contact

For questions or issues, please contact:

- vaadhishree@gmail.com
- karthikapanchu2004@gmail.com
- lakshanikasekhar.pro@gmail.com
- sansitakarthik2005@gmail.com
