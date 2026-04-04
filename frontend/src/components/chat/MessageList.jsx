import ReactMarkdown from "react-markdown";

function ThinkingMessage() {
  return (
    <div className="msg-wrap ai">
      <div className="msg-role">OctoSearch</div>
      <div className="thinking-bubble">
        thinking
        <div className="dots">
          <span />
          <span />
          <span />
        </div>
      </div>
    </div>
  );
}

function SourceChips({ sources }) {
  if (!sources || sources.length === 0) {
    return null;
  }

  return (
    <div className="sources-row">
      {sources.map((source, index) => (
        <span key={`${source.path}-${index}`} className="source-chip">
          {source.path}
        </span>
      ))}
    </div>
  );
}

export default function MessageList({ messages, isThinking, messagesEndRef }) {
  if (messages.length === 0 && !isThinking) {
    return (
      <div className="empty-hint">
        Ask anything about the codebase - architecture, functions, dependencies.
      </div>
    );
  }

  return (
    <div className="messages">
      {messages.map((message, index) => (
        <div key={`${message.role}-${index}`} className={`msg-wrap ${message.role}`}>
          <div className="msg-role">{message.role === "user" ? "You" : "OctoSearch"}</div>
          <div className="msg-bubble">
            <ReactMarkdown>{message.text}</ReactMarkdown>
            <SourceChips sources={message.sources} />
          </div>
        </div>
      ))}

      {isThinking && <ThinkingMessage />}
      <div ref={messagesEndRef} />
    </div>
  );
}
