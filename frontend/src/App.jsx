import { useEffect, useRef, useState } from "react";
import ChatPanel from "./components/chat/ChatPanel";
import AppHeader from "./components/layout/AppHeader";
import LoadingProgress from "./components/load/LoadingProgress";
import RepoConnect from "./components/load/RepoConnect";
import { INDEXING_STEPS, PHASES } from "./constants/app";
import { askCodebase, loadRepository } from "./services/octoApi";
import "./styles/app.css";

export default function App() {
  const [phase, setPhase] = useState(PHASES.LOAD);
  const [repoUrl, setRepoUrl] = useState("");
  const [repoLabel, setRepoLabel] = useState("");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const messagesEndRef = useRef(null);
  const queryInputRef = useRef(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, isThinking]);

  useEffect(() => {
    if (phase === PHASES.CHAT && queryInputRef.current) {
      queryInputRef.current.focus();
    }
  }, [phase]);

  const loadRepo = async () => {
    const url = repoUrl.trim();
    if (!url) {
      return;
    }

    const parts = url.replace(/\/$/, "").split("/");
    setRepoLabel(parts.slice(-2).join("/") || url);
    setPhase(PHASES.LOADING);
    setActiveStep(0);

    const stepTimer = setInterval(() => {
      setActiveStep((previous) => {
        if (previous < INDEXING_STEPS.length - 2) {
          return previous + 1;
        }

        clearInterval(stepTimer);
        return previous;
      });
    }, 1600);

    try {
      await loadRepository(url);
    } catch (_) {
      // Keep the current optimistic flow and let users query after indexing transition.
    }

    clearInterval(stepTimer);
    setActiveStep(INDEXING_STEPS.length - 1);
    setTimeout(() => setPhase(PHASES.CHAT), 700);
  };

  const sendQuery = async () => {
    const normalizedQuery = query.trim();
    if (!normalizedQuery || isThinking) {
      return;
    }

    setMessages((previous) => [...previous, { role: "user", text: normalizedQuery }]);
    setQuery("");
    setIsThinking(true);

    try {
      const data = await askCodebase(normalizedQuery);
      setMessages((previous) => [
        ...previous,
        {
          role: "ai",
          text: data.message ?? data.answer,
          sources: data.sources ?? [],
        },
      ]);
    } catch (_) {
      setMessages((previous) => [
        ...previous,
        {
          role: "ai",
          text: "Could not reach the server. Make sure the backend is running on port 8000.",
          sources: [],
        },
      ]);
    } finally {
      setIsThinking(false);
    }
  };

  return (
    <div className="wrap">
      <AppHeader />

      {phase === PHASES.LOAD && (
        <RepoConnect repoUrl={repoUrl} onRepoUrlChange={setRepoUrl} onSubmit={loadRepo} />
      )}

      {phase === PHASES.LOADING && (
        <LoadingProgress repoLabel={repoLabel} steps={INDEXING_STEPS} activeStep={activeStep} />
      )}

      {phase === PHASES.CHAT && (
        <ChatPanel
          repoLabel={repoLabel}
          messages={messages}
          isThinking={isThinking}
          messagesEndRef={messagesEndRef}
          query={query}
          queryInputRef={queryInputRef}
          onQueryChange={setQuery}
          onSendQuery={sendQuery}
        />
      )}
    </div>
  );
}