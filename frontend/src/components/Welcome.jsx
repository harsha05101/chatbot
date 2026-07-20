import React from "react";

function Welcome({ onOptionSelect }) {
  return (
    <div className="welcome">
      <div className="shield">🛡️</div>
      <h2>Welcome to PhishGuard AI</h2>
      <p style={{ color: "#8696a0", marginTop: "8px" }}>
        Select a detection category or paste content below to start scanning for threats.
      </p>

      <div className="options">
        <button onClick={() => onOptionSelect("Email")}>
          <span style={{ fontSize: "1.4rem" }}>📧</span>
          <span>Analyze Email</span>
        </button>
        
        <button onClick={() => onOptionSelect("SMS")}>
          <span style={{ fontSize: "1.4rem" }}>💬</span>
          <span>Analyze SMS</span>
        </button>

        <button onClick={() => onOptionSelect("URL")}>
          <span style={{ fontSize: "1.4rem" }}>🌐</span>
          <span>Analyze URL</span>
        </button>

        <button onClick={() => onOptionSelect("Screenshot")}>
          <span style={{ fontSize: "1.4rem" }}>🖼️</span>
          <span>Screenshot</span>
        </button>
      </div>
    </div>
  );
}

export default Welcome;