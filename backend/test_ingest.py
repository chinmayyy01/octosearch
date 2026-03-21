from ingest import load_repo

if __name__ == "__main__":
    repo_url = "https://github.com/psf/requests"  
    
    data = load_repo(repo_url)
    
    print(f"\nTotal files loaded: {len(data)}\n")
    
    for i in range(min(3, len(data))):
        print(f"File {i+1}: {data[i]['path']}")
        print(f"Content preview:\n{data[i]['content'][:200]}")
        print("-" * 50)