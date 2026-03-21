import subprocess
import os
from utils.file_loader import get_code_files, load_file_content

def clone_repo(repo_url, target_dir="data/repos"):
    os.makedirs(target_dir, exist_ok=True)
    
    repo_name = repo_url.split("/")[-1].replace(".git", "")
    repo_path = os.path.join(target_dir, repo_name)
    
    if os.path.exists(repo_path):
        print("Repo already exists.")
        return repo_path
    
    subprocess.run(["git", "clone", repo_url, repo_path])
    return repo_path

def load_repo(repo_url):
    repo_path = clone_repo(repo_url)
    
    files = get_code_files(repo_path)
    data = []
    
    for f in files:
        content = load_file_content(f)
        if content:
            data.append({
                "path": os.path.relpath(f, repo_path),
                "content": content
            })
    return data