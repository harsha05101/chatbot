function ChatBubble({ sender, text }) {

  return (

    <div
      className={
        sender === "user"
          ? "chat-bubble user"
          : "chat-bubble bot"
      }
    >

      <pre
        style={{
          whiteSpace: "pre-wrap",
          fontFamily: "inherit",
        }}
      >
        {text}
      </pre>

    </div>

  );

}

export default ChatBubble;