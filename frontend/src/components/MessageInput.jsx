import { useState, useRef } from "react";
import API from "../services/api";
import { isGreeting } from "../utils/greetings";

function MessageInput({ setMessages }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const fileInputRef = useRef(null);

  async function sendMessage() {
    if (input.trim() === "" || loading) return;

    const userMessage = input;

    // 1. Add user message bubble
    setMessages((prev) => [
      ...prev,
      { sender: "user", text: userMessage },
    ]);

    setInput("");

    // 2. Handle Greetings
    if (isGreeting(userMessage)) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `👋 Welcome to PhishGuard AI!\n\nChoose one of the following:\n\n📧 Analyze Email\n💬 Analyze SMS\n🌐 Analyze URL\n🖼️ Analyze Screenshot`,
        },
      ]);
      return;
    }

    // 3. API Call to Backend
    try {
      setLoading(true);
      const response = await API.post("/analyze", { message: userMessage });
      const data = response.data;

      const reasonsList = data.reasons && data.reasons.length > 0 
        ? data.reasons.map((r) => `• ${r}`).join("\n") 
        : "• No explicit anomaly patterns detected.";

      const botReply = `
🛡️ Risk Level: ${data.risk_level} (${data.risk_score}/100)
🏷️ Category: ${data.category}
📊 Similarity Score: ${data.similarity}%

📌 Reasons Identified:
${reasonsList}

🤖 AI Analysis & Advice:
${data.explanation}
`;

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: botReply.trim() },
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❌ Unable to analyze the message. Please ensure the backend is running." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // Handle Image Upload & OCR
  async function handleFileUpload(e) {
    const file = e.target.files[0];
    if (!file) return;

    setMessages((prev) => [
      ...prev,
      { sender: "user", text: `🖼️ Uploaded image: ${file.name}` },
      { sender: "bot", text: "🔍 Extracting text from screenshot via OCR..." }
    ]);

    const formData = new FormData();
    formData.append("file", file);

    try {
      setLoading(true);
      // Send file to Flask /upload route
      const ocrRes = await API.post("/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });

      const extractedText = ocrRes.data.extracted_text;

      if (!extractedText || !extractedText.trim()) {
        setMessages((prev) => [
          ...prev,
          { sender: "bot", text: "⚠️ No clear text could be read from this screenshot." }
        ]);
        return;
      }

      // Automatically run extracted text through /analyze
      const analyzeRes = await API.post("/analyze", { message: extractedText });
      const data = analyzeRes.data;

      const botReply = `
📄 Extracted Text: "${extractedText}"

🛡️ Risk Level: ${data.risk_level} (${data.risk_score}/100)
🏷️ Category: ${data.category}
📊 Similarity Score: ${data.similarity}%

📌 Reasons Identified:
${data.reasons?.map((r) => `• ${r}`).join("\n") || "• None"}

🤖 AI Analysis & Advice:
${data.explanation}
`;

      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: botReply.trim() }
      ]);
    } catch (error) {
      console.error(error);
      setMessages((prev) => [
        ...prev,
        { sender: "bot", text: "❌ Failed to process screenshot. Ensure Tesseract OCR is installed on your computer." }
      ]);
    } finally {
      setLoading(false);
      if (fileInputRef.current) fileInputRef.current.value = "";
    }
  }

  return (
    <div className="message-input">
      <input
        type="text"
        placeholder="Paste email, SMS or URL..."
        value={input}
        disabled={loading}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={(e) => {
          if (e.key === "Enter") sendMessage();
        }}
      />

      {/* Hidden File Input */}
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileUpload}
        accept="image/*"
        style={{ display: "none" }}
      />

      {/* Paperclip Button */}
      <button 
        type="button" 
        onClick={() => fileInputRef.current?.click()} 
        disabled={loading}
        title="Upload Screenshot"
      >
        📎
      </button>

      {/* Send Button */}
      <button type="button" onClick={sendMessage} disabled={loading}>
        ➤
      </button>
    </div>
  );
}

export default MessageInput;