export default function LoadingProgress({ repoLabel, steps, activeStep }) {
  return (
    <section className="phase-loading">
      <div>
        <p className="loading-title">Indexing repository</p>
        <p className="loading-repo">{repoLabel}</p>
      </div>

      <div className="steps">
        {steps.map((label, index) => {
          const isDone = index < activeStep;
          const isActive = index === activeStep;

          return (
            <div
              key={label}
              className={`step-row${isDone ? " done" : isActive ? " active" : ""}`}
            >
              <div className="step-indicator">{isDone && <span>&#10003;</span>}</div>
              {label}
            </div>
          );
        })}
      </div>
    </section>
  );
}
