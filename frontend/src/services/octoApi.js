const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000").replace(/\/$/, "");

async function fetchWithTimeout(url, options = {}, timeoutMs = 30000) {
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), timeoutMs);

  try {
    const response = await fetch(url, { ...options, signal: controller.signal });
    return response;
  } finally {
    clearTimeout(timeoutId);
  }
}

export async function loadRepository(repoUrl, options = {}) {
  const timeoutMs = options.timeoutMs ?? 15000;
  const response = await fetchWithTimeout(
    `${API_BASE_URL}/load_repo`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl }),
    },
    timeoutMs,
  );

  if (!response.ok) {
    throw new Error(`Load repo failed with status ${response.status}`);
  }

  return response.json();
}

export async function askCodebase(question, options = {}) {
  const timeoutMs = options.timeoutMs ?? 45000;
  const response = await fetchWithTimeout(
    `${API_BASE_URL}/query`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: question }),
    },
    timeoutMs,
  );

  if (!response.ok) {
    throw new Error(`Query failed with status ${response.status}`);
  }

  return response.json();
}

export async function getBackendHealth(options = {}) {
  const timeoutMs = options.timeoutMs ?? 8000;
  const response = await fetchWithTimeout(`${API_BASE_URL}/`, { method: "GET" }, timeoutMs);

  if (!response.ok) {
    throw new Error(`Health check failed with status ${response.status}`);
  }

  return response.json();
}
