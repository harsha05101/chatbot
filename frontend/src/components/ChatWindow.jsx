import React from "react";

function ChatWindow({ messages = [] }) {
  return (
    <div className="chat-window">
      {messages.map((msg, index) => (
        <div
          key={index}
          className={msg.sender === "user" ? "user-message" : "bot-message"}
        >
          <div className="message">
            {msg.text}
          </div>
        </div>
      ))}
    </div>
  );
}

export default ChatWindow;