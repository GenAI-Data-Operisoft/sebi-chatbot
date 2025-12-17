import React, { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import './App.css';

// ✅ Use env variable for prod, fallback for local
const API_BASE_URL =
  process.env.REACT_APP_API_URL || 'http://65.0.117.13:8000';

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'bot',
      content:
        "Hello! I'm your SEBI cybersecurity assistant. Ask me anything about SEBI policies, regulations, and cybersecurity frameworks.",
      timestamp: new Date(),
    },
  ]);

  const [currentMessage, setCurrentMessage] = useState('');
  const [loading, setLoading] = useState(false);
  const [topK, setTopK] = useState(4);

  const messagesEndRef = useRef(null);
  const inputRef = useRef(null);

  // ---------- Auto scroll ----------
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // ---------- Format time safely ----------
  const formatTime = (timestamp) => {
    const date = timestamp instanceof Date ? timestamp : new Date(timestamp);
    return date.toLocaleTimeString([], {
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  // ---------- Submit message ----------
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!currentMessage.trim() || loading) return;

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: currentMessage.trim(),
      timestamp: new Date(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setCurrentMessage('');
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/ask`, {
        question: userMessage.content,
        top_k: topK,
      });

      const botMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content: response.data.answer,
        timestamp: new Date(),
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'bot',
        content:
          err.response?.data?.detail ||
          'Failed to get answer. Please try again.',
        timestamp: new Date(),
        isError: true,
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  // ---------- Clear chat ----------
  const handleClear = () => {
    setMessages([
      {
        id: 1,
        type: 'bot',
        content:
          "Hello! I'm your SEBI cybersecurity assistant. Ask me anything about SEBI policies, regulations, and cybersecurity frameworks.",
        timestamp: new Date(),
      },
    ]);
  };

  // ---------- Enter key handling ----------
  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <div className="App">
      {/* ---------- Header ---------- */}
      <header className="App-header">
        <div className="header-content">
          <h1>🛡️ SEBI Cybersecurity Assistant</h1>
          <p>Your AI-powered guide to SEBI policies and regulations</p>
        </div>

        <div className="settings-panel">
          <label htmlFor="topK">Sources:</label>
          <select
            id="topK"
            value={topK}
            onChange={(e) => setTopK(Number(e.target.value))}
            disabled={loading}
          >
            <option value={2}>2</option>
            <option value={4}>4</option>
            <option value={6}>6</option>
            <option value={8}>8</option>
          </select>

          <button
            onClick={handleClear}
            className="clear-btn"
            disabled={loading}
          >
            🗑️ Clear Chat
          </button>
        </div>
      </header>

      {/* ---------- Chat ---------- */}
      <main className="chat-container">
        <div className="messages-container">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`message ${message.type}-message ${
                message.isError ? 'error' : ''
              }`}
            >
              <div className="message-avatar">
                {message.type === 'user' ? '👤' : '🤖'}
              </div>

              <div className="message-content">
                <div className="message-text">{message.content}</div>
                <div className="message-time">
                  {formatTime(message.timestamp)}
                </div>
              </div>
            </div>
          ))}

          {/* ---------- Typing Indicator ---------- */}
          {loading && (
            <div className="message bot-message typing">
              <div className="message-avatar">🤖</div>
              <div className="message-content">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                <div className="message-time">Typing...</div>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* ---------- Input ---------- */}
        <form onSubmit={handleSubmit} className="input-form">
          <div className="input-container">
            <textarea
              ref={inputRef}
              value={currentMessage}
              onChange={(e) => setCurrentMessage(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask me about SEBI cybersecurity policies..."
              rows={1}
              disabled={loading}
              className="message-input"
            />

            <button
              type="submit"
              disabled={loading || !currentMessage.trim()}
              className="send-button"
            >
              {loading ? '⏳' : '📤'}
            </button>
          </div>
        </form>
      </main>
    </div>
  );
}

export default App;
