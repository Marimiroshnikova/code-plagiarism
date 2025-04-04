import json
from pathlib import Path
import logging

REPO_DIR = Path("data/repositories")
OUTPUT_FILE = Path("data/file_index.json")

def find_code_files():
    code_extensions = {".py", ".java", ".c", ".cpp", ".js"}
    file_index = []

    for repo_path in REPO_DIR.iterdir():
        if repo_path.is_dir():
            for file_path in repo_path.rglob("*"):
                if file_path.suffix in code_extensions and file_path.is_file():
                    try:
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        file_index.append({
                            "path": str(file_path.relative_to(REPO_DIR)),
                            "content": content
                        })
                    except Exception as e:
                        logging.warning(f"Error reading {file_path}: {e}")

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(file_index, f, indent=2)
    
    print(f"Indexed {len(file_index)} code files")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    find_code_files()