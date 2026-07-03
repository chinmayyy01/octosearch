import os
import requests
from backend.utils.file_loader import VALID_EXTENSIONS

def load_repo(repo_url):
    if not repo_url.startswith("https://github.com/"):
        raise ValueError("Only GitHub repositories are supported")

    parts = repo_url.replace("https://github.com/", "").replace(".git", "").split("/")
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")

    owner, repo = parts[0], parts[1]
    github_token = os.getenv("GITHUB_TOKEN")

    headers = {}
    if github_token:
        headers["Authorization"] = f"token {github_token}"

    api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    response = requests.get(api_url, headers=headers)

    if response.status_code == 404:
        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/master?recursive=1"
        response = requests.get(api_url, headers=headers)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch repository tree: {response.status_code}")

    tree = response.json()
    data = []

    for item in tree.get("tree", []):
        if item["type"] == "blob":
            path = item["path"]
            if any(path.endswith(ext) for ext in VALID_EXTENSIONS):
                file_url = item["url"]
                file_response = requests.get(file_url, headers=headers)
                if file_response.status_code == 200:
                    content = file_response.json().get("content", "")
                    if content:
                        import base64
                        try:
                            decoded_content = base64.b64decode(content).decode("utf-8")
                            data.append({
                                "path": path,
                                "content": decoded_content
                            })
                        except:
                            continue

    return data