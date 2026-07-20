import React, { useState } from "react";
import Welcome from "./components/Welcome";
import ChatWindow from "./components/ChatWindow";
import MessageInput from "./components/MessageInput";

function App() {
  const [messages, setMessages] = useState([]);

  // Clear messages to go back to Options Page
  const handleResetToOptions = () => {
    setMessages([]);
  };

  // Pre-fill chat when an Option button is clicked
  const handleOptionSelect = (type) => {
    const defaultPrompts = {
      Email: "Please paste the suspicious email content below.",
      SMS: "Please paste the SMS message below.",
      URL: "Please paste the suspicious web link (URL) below.",
      Screenshot: "Click the attachment button 📎 below to upload an image screenshot.",
    };

    setMessages([
      {
        sender: "bot",
        text: `🔍 **${type} Analysis Mode Activated**\n\n${defaultPrompts[type] || "Paste your input below."}`,
      },
    ]);
  };

  return (
    <div className="app">
      {/* Top Navbar Header */}
      <header className="header">
        <h1>🛡️ PhishGuard AI</h1>
        {messages.length > 0 && (
          <button className="header-btn" onClick={handleResetToOptions}>
            🏠 Back to Options
          </button>
        )}
      </header>

      <div className="main-container">
        {/* Left Sidebar */}
        <div className="sidebar">
          <button onClick={handleResetToOptions}>➕ New Analysis</button>
          <button onClick={() => handleOptionSelect("Email")}>📧 Analyze Email</button>
          <button onClick={() => handleOptionSelect("SMS")}>💬 Analyze SMS</button>
          <button onClick={() => handleOptionSelect("URL")}>🌐 Analyze URL</button>
          <button onClick={() => handleOptionSelect("Screenshot")}>🖼️ Screenshot OCR</button>
        </div>

        {/* Center Content View */}
        <div className="chat-section">
          {messages.length === 0 ? (
            /* Options Screen when no chat history */
            <Welcome onOptionSelect={handleOptionSelect} />
          ) : (
            /* Active Oval Chat Window */
            <ChatWindow messages={messages} />
          )}

          {/* Input Bar */}
          <MessageInput setMessages={setMessages} />
        </div>
      </div>
    </div>
  );
}

export default App;