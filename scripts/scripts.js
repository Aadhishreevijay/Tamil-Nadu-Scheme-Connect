// Function to send a message to the chatbot
function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    const messagesContainer = document.getElementById('messages');

    // Display user's message
    const userMessageElement = document.createElement('div');
    userMessageElement.className = 'message user';
    userMessageElement.textContent = 'You: ' + userInput;
    messagesContainer.appendChild(userMessageElement);

    // Send message to the backend
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Display the chatbot's response
        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'message assistant';
        botMessageElement.innerHTML = `Bot: ${data.response}`;

        // Display sources
        if (data.sources && data.sources.length > 0) {
            botMessageElement.innerHTML += '<br>Sources: <ul>' + data.sources.map(s => `<li><a href="${s}" target="_blank">${s}</a></li>`).join('') + '</ul>';
        }

        messagesContainer.appendChild(botMessageElement);

        // Save chat history
        saveChatHistory(userInput, data.response);
    });

    // Clear the input field
    document.getElementById('user-input').value = '';
}

// Function to save chat history to local storage
function saveChatHistory(userMessage, botResponse) {
    const timestamp = new Date().toLocaleString();
    let chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];
    chatHistory.push({ userMessage, botResponse, timestamp });
    localStorage.setItem('chatHistory', JSON.stringify(chatHistory));
    loadChatHistory('newest'); // Update history panel immediately with newest first
}

// Function to load chat history based on the order parameter
function loadChatHistory(order) {
    console.log('Loading chat history', order);
    const historyMessagesContainer = document.getElementById('history-messages');
    const chatHistory = JSON.parse(localStorage.getItem('chatHistory')) || [];

    historyMessagesContainer.innerHTML = ''; // Clear existing history

    if (order === 'newest') {
        chatHistory.reverse(); // Show newest first
    }

    chatHistory.forEach(chat => {
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'message user';
        userMessageElement.innerHTML = `<strong>You:</strong> ${chat.userMessage} <span class="timestamp">${chat.timestamp}</span>`;
        historyMessagesContainer.appendChild(userMessageElement);

        const botMessageElement = document.createElement('div');
        botMessageElement.className = 'message assistant';
        botMessageElement.innerHTML = `<strong>Bot:</strong> ${chat.botResponse} <span class="timestamp">${chat.timestamp}</span>`;
        historyMessagesContainer.appendChild(botMessageElement);
    });
}

// Function to handle dropdown change
function changeOrder() {
    const selectedOrder = document.getElementById('sort-dropdown').value;
    loadChatHistory(selectedOrder);
}

// Load chat history on page load
window.onload = function() {
    loadChatHistory('newest'); // Default to newest first
};

// Event listener for dropdown change
document.getElementById('sort-dropdown').addEventListener('change', changeOrder);

// Speech Recognition functionality
const micButton = document.getElementById('voice-button');
micButton.addEventListener('click', function() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US';

    recognition.onresult = function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('user-input').value = transcript;
    };

    recognition.start();
});
