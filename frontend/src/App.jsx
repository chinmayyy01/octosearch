import { useEffect, useRef, useState } from "react";
import ChatPanel from "./components/chat/ChatPanel";
import AppHeader from "./components/layout/AppHeader";
import LoadingProgress from "./components/load/LoadingProgress";
import RepoConnect from "./components/load/RepoConnect";
import { INDEXING_STEPS, PHASES } from "./constants/app";
import { askCodebase, getBackendHealth, loadRepository } from "./services/octoApi";
import "./styles/app.css";

export default function App() {
  const [phase, setPhase] = useState(PHASES.LOAD);
  const [repoUrl, setRepoUrl] = useState("");
  const [repoLabel, setRepoLabel] = useState("");
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [isThinking, setIsThinking] = useState(false);
  const [activeStep, setActiveStep] = useState(0);
  const [backendStatus, setBackendStatus] = useState("checking");
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

  useEffect(() => {
    if (phase !== PHASES.LOADING && phase !== PHASES.CHAT) {
      return undefined;
    }

    let isMounted = true;

    const syncBackendStatus = async () => {
      try {
        const health = await getBackendHealth();
        if (!isMounted) {
          return;
        }

        const normalized = health?.status === "ready" ? "ready" : "building";
        setBackendStatus(normalized);
      } catch (_) {
        if (isMounted) {
          setBackendStatus("offline");
        }
      }
    };

    syncBackendStatus();
    const poll = setInterval(syncBackendStatus, 5000);

    return () => {
      isMounted = false;
      clearInterval(poll);
    };
  }, [phase]);

  const loadRepo = async () => {
    const url = repoUrl.trim();
    if (!url) {
      return;
    }

    const parts = url.replace(/\/$/, "").split("/");
    setRepoLabel(parts.slice(-2).join("/") || url);
    setPhase(PHASES.LOADING);
    setBackendStatus("building");
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
      setMessages((previous) => [
        ...previous,
        {
          role: "ai",
          text: "Indexing has started but the server is still waking up or processing. You can continue to chat; if indexing is not ready yet, I will tell you to wait.",
          sources: [],
        },
      ]);
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
    } catch (error) {
      const isTimeout = error?.name === "AbortError";
      setMessages((previous) => [
        ...previous,
        {
          role: "ai",
          text: isTimeout
            ? "The backend is taking too long to respond (likely cold start or heavy indexing). Please wait a bit and try again."
            : "Could not reach the server. Make sure the backend is running and accessible.",
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
          backendStatus={backendStatus}
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