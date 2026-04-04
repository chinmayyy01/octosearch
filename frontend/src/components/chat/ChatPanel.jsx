import MessageList from "./MessageList";
import QueryComposer from "./QueryComposer";

export default function ChatPanel({
  repoLabel,
  messages,
  isThinking,
  messagesEndRef,
  query,
  queryInputRef,
  onQueryChange,
  onSendQuery,
}) {
  return (
    <section className="phase-chat">
      <div className="repo-tag">
        <div className="live-dot" />
        {repoLabel}
      </div>

      <MessageList messages={messages} isThinking={isThinking} messagesEndRef={messagesEndRef} />

      <QueryComposer
        query={query}
        isThinking={isThinking}
        queryInputRef={queryInputRef}
        onChange={onQueryChange}
        onSubmit={onSendQuery}
      />
    </section>
  );
}
