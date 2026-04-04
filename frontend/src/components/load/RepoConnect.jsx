export default function RepoConnect({ repoUrl, onRepoUrlChange, onSubmit }) {
  return (
    <section className="phase-load">
      <p className="load-label">Step 1 of 2 - Connect</p>
      <p className="load-description">
        Paste a public GitHub repository URL to index its codebase. Once loaded, you can ask
        questions about its structure, logic, and patterns.
      </p>
      <div className="input-row">
        <input
          className="field"
          type="text"
          value={repoUrl}
          onChange={(event) => onRepoUrlChange(event.target.value)}
          onKeyDown={(event) => event.key === "Enter" && onSubmit()}
          placeholder="https://github.com/owner/repository"
        />
        <button className="btn-primary" onClick={onSubmit} disabled={!repoUrl.trim()}>
          Load Repo
        </button>
      </div>
    </section>
  );
}
