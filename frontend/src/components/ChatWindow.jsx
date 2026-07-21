import React, { useEffect, useRef } from "react";

function ChatWindow({ messages = [] }) {
  const messagesEndRef = useRef(null);

  // Auto-scroll to the bottom whenever a new message arrives
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

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
      {/* Invisible element to anchor automatic scrolling */}
      <div ref={messagesEndRef} />
    </div>
  );
}

export default ChatWindow;