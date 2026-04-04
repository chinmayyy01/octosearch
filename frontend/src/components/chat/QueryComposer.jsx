export default function QueryComposer({ query, isThinking, queryInputRef, onChange, onSubmit }) {
  return (
    <div className="query-bar">
      <input
        ref={queryInputRef}
        className="query-input"
        value={query}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={(event) => event.key === "Enter" && onSubmit()}
        placeholder="Ask about the codebase..."
        disabled={isThinking}
      />
      <button className="btn-send" onClick={onSubmit} disabled={!query.trim() || isThinking}>
        <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
          <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z" />
        </svg>
      </button>
    </div>
  );
}
