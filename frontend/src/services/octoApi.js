const API_BASE_URL = "http://127.0.0.1:8000";

export async function loadRepository(repoUrl) {
  const response = await fetch(`${API_BASE_URL}/load_repo`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ repo_url: repoUrl }),
  });

  return response;
}

export async function askCodebase(question) {
  const response = await fetch(`${API_BASE_URL}/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: question }),
  });

  if (!response.ok) {
    throw new Error(`Query failed with status ${response.status}`);
  }

  return response.json();
}
