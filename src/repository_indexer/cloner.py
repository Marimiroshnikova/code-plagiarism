import subprocess
from pathlib import Path
import os

REPO_DIR = Path("data/repositories")
REPOS_FILE = Path("configs/repositories.txt")

def clone_repositories():
    REPO_DIR.mkdir(parents=True, exist_ok=True)
    
    with open(REPOS_FILE) as f:
        repos = [line.strip() for line in f if line.strip()]
        
    for repo_url in repos:
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        target_dir = REPO_DIR / repo_name
        
        try:
            if not target_dir.exists():
                print(f"Cloning {repo_name}...")
                subprocess.run(
                    ["git", "clone", "--depth", "1", repo_url, str(target_dir)], 
                    check=True
                )
                print(f"✅ Success: {repo_name}")
            else:
                print(f"⚠️ Already exists: {repo_name}")
        except Exception as e:
            print(f"❌ Error cloning {repo_name}: {str(e)}")

if __name__ == "__main__":
    print("\n=== Starting repository cloning ===")
    clone_repositories()
    print("=== Process completed ===\n")