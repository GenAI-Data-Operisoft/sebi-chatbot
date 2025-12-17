# SEBI Cybersecurity Chatbot

An AI-powered chatbot built with React that provides interactive conversations about SEBI cybersecurity policies and regulations. The chatbot interfaces with a FastAPI backend powered by AWS Bedrock and FAISS vector search.

## Features

- 💬 **Interactive Chat Interface** - Real-time conversation with AI assistant
- 🔍 **Intelligent Search** - Powered by FAISS vector search across SEBI documents
- 🤖 **AI Responses** - Uses AWS Bedrock (Claude 3 Haiku) for natural language responses
- 📱 **Responsive Design** - Works seamlessly on desktop and mobile devices
- ⚙️ **Configurable Sources** - Adjust number of document sources (2-8) for responses
- 💾 **Chat History** - Maintains conversation history during session
- ⚡ **Real-time Typing Indicators** - Shows when AI is processing responses
- 🎨 **Modern UI** - Beautiful gradient design with smooth animations

## Prerequisites

- Node.js (version 14 or higher)
- npm or yarn
- Running FastAPI backend (main.py)

## Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The application will open in your browser at `http://localhost:3000`.

## Backend Setup

Make sure your FastAPI backend is running on `http://localhost:8000`. To start the backend:

```bash
# Install Python dependencies
pip install -r requirements.txt

# Start the FastAPI server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Usage

1. **Start Chatting**: Type your question about SEBI cybersecurity policies in the input field
2. **Send Message**: Press Enter or click the send button (📤)
3. **Adjust Settings**: Use the dropdown in the header to change number of sources (2-8)
4. **View Responses**: AI responses appear in real-time with typing indicators
5. **Clear History**: Click "🗑️ Clear Chat" to start a new conversation
6. **Mobile Support**: Works great on phones and tablets with touch-friendly interface

## API Integration

The React app communicates with the FastAPI backend through:
- **Endpoint**: `POST /ask`
- **Request**: `{ "question": "string", "top_k": number }`
- **Response**: `{ "answer": "string" }`

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm build` - Builds the app for production
- `npm test` - Launches the test runner
- `npm eject` - Ejects from Create React App (one-way operation)

## Project Structure

```
Frontend/
├── public/
│   └── index.html      # HTML template
├── src/
│   ├── App.js          # Main chatbot component
│   ├── App.css         # Chatbot styling
│   ├── index.js        # React entry point
│   └── index.css       # Global styles
├── package.json        # Dependencies and scripts
└── README.md          # Documentation

Backend/
├── main.py            # FastAPI server with Bedrock integration
├── loader.py          # Document processing utilities
├── requirements.txt   # Python dependencies
├── data/             # SEBI PDF documents
├── textract_text/    # Extracted text files
└── vectorstore/      # FAISS vector database
```

## Customization

- Modify `API_BASE_URL` in `App.js` if your backend runs on a different port
- Adjust styling in `App.css` to match your branding
- Add additional form fields or features as needed
## Ch
atbot Features

### 🎯 Smart Conversations
- Maintains context within the current session
- Provides source-based answers from SEBI documents
- Handles errors gracefully with user-friendly messages

### 🎨 User Experience
- **Typing Indicators**: See when the AI is thinking
- **Message Timestamps**: Track conversation flow
- **Emoji Avatars**: User (👤) and Bot (🤖) identification
- **Smooth Animations**: Messages slide in naturally
- **Auto-scroll**: Always shows the latest messages

### 📱 Mobile Optimized
- Touch-friendly interface
- Responsive design for all screen sizes
- Optimized input handling for mobile keyboards
- Swipe-friendly scrolling

### ⚙️ Customizable
- Adjust number of document sources for more comprehensive answers
- Clear chat history to start fresh conversations
- Real-time settings changes without page reload

## Sample Questions to Try

- "What are the key cybersecurity requirements for stock brokers?"
- "Tell me about SEBI's cloud adoption framework"
- "What are the incident reporting requirements?"
- "Explain the cyber resilience framework"
- "What are the best practices for cybersecurity audits?"

## Technical Details

- **Frontend**: React 18 with modern hooks (useState, useEffect, useRef)
- **Styling**: Custom CSS with gradients, animations, and responsive design
- **API Communication**: Axios for HTTP requests
- **Real-time Updates**: Automatic scrolling and typing indicators
- **Error Handling**: Comprehensive error states and user feedback