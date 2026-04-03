import { useState } from "react";
import ReactMarkdown from "react-markdown";

export default function App() {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [repoUrl, setRepoUrl] = useState("");

  const sendQuery = async () => {
    if (!query) return;

    const newMessages = [...messages, { role: "user", text: query }];
    setMessages(newMessages);

    setQuery("");

    const res = await fetch("http://127.0.0.1:8000/query", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ query }),
    });

    const data = await res.json();

    if (data.message) {
      setMessages([
        ...newMessages,
        { role: "ai", text: data.message, sources: [] },
      ]);
      return;
    }

    setMessages([
      ...newMessages,
      {
        role: "ai",
        text: data.answer,
        sources: data.sources,
      },
    ]);
  };

  return (
    <div className="min-h-screen bg-slate-900 text-white flex justify-center">
      <div className="w-full max-w-2xl p-6">
        <h1 className="text-3xl font-bold mb-4">🐙 OctoSearch</h1>

        <div className="space-y-4">
          {messages.map((msg, i) => (
            <div
              key={i}
              className={`p-3 rounded ${
                msg.role === "user"
                  ? "bg-blue-600"
                  : "bg-slate-700"
              }`}
            >
              <div className="prose prose-invert max-w-none">
                <ReactMarkdown>{msg.text}</ReactMarkdown>
              </div>

              {msg.sources && msg.sources.length > 0 && (
                <div className="mt-2 text-sm text-slate-300">
                  <b>Sources:</b>
                  {msg.sources.map((s, idx) => (
                    <div key={idx}>{s.path}</div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>

        <input
          className="w-full p-2 rounded text-black mb-2"
          value={repoUrl}
          onChange={(e) => setRepoUrl(e.target.value)}
          placeholder="Enter GitHub repo URL"
        />

        <button
          onClick={async () => {
            await fetch("http://127.0.0.1:8000/load_repo", {
              method: "POST",
              headers: {
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ repo_url: repoUrl }),
            });

            alert("Repo loading started. Wait a few seconds.");
          }}
          className="bg-purple-600 px-4 py-2 rounded mb-4"
        >
          Load Repo
        </button>
        
        <div className="mt-6 flex gap-2">
          <input
            className="flex-1 p-2 rounded text-black"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about the codebase..."
          />
          <button
            onClick={sendQuery}
            className="bg-green-600 px-4 rounded"
          >
            Ask
          </button>
        </div>
      </div>
    </div>
  );
}