import os
from pathspec import PathSpec
from pathspec.patterns import GitWildMatchPattern

VALID_EXTENSIONS = [".py", ".js", ".ts", ".java", ".cpp", ".c", ".go", ".rs", ".rb", ".php", ".cs", ".swift", ".kt", ".jsx", ".tsx"]

DEFAULT_IGNORE = [".git", "node_modules", "venv", "__pycache__", "dist", "build"]

MAX_FILE_SIZE = 500_000  # 500 KB

def load_gitignore(repo_path):
    gitignore_path = os.path.join(repo_path, ".gitignore")
    
    if not os.path.exists(gitignore_path):
        return None
    
    with open(gitignore_path, "r") as f:
        patterns = f.read().splitlines()
        
    return PathSpec.from_lines(GitWildMatchPattern, patterns)

def should_ignore(path, repo_path, gitignore_spec):
    rel_path = os.path.relpath(path, repo_path)
    
    for ignore in DEFAULT_IGNORE:
        if ignore in rel_path:
            return True
    if gitignore_spec and gitignore_spec.match_file(rel_path):
        return True
    return False
    
def get_code_files(repo_path):
    code_files = []
    gitignore_spec = load_gitignore(repo_path)
    
    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if not should_ignore(os.path.join(root, d), repo_path, gitignore_spec)]
        
        for file in files:
            file_path = os.path.join(root, file)
            if should_ignore(file_path, repo_path, gitignore_spec):
                continue
            if not any(file.endswith(ext) for ext in VALID_EXTENSIONS):
                continue
            try:
                if os.path.getsize(file_path) > MAX_FILE_SIZE:
                    continue
            except:
                continue
            code_files.append(file_path)
    return code_files

def load_file_content(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None