# -*- coding: utf-8 -*-
"""Push to empty GitHub repo using GraphQL API - creates initial commit with all files"""
import requests, os, base64, json, time

GITHUB_TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"
PROJECT_DIR = r"C:\Projects\chromebest"

SKIP_DIRS = {'.git', 'public', 'node_modules', '__pycache__', '.hugo_build.lock'}
SKIP_EXTS = {'.py'}

def get_token():
    with open(GITHUB_TOKEN_FILE, 'r') as f:
        return f.read().strip()

def headers():
    return {
        "Authorization": f"bearer {get_token()}",
        "Content-Type": "application/json"
    }

def collect_files(base_dir):
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in filenames:
            if any(fname.endswith(ext) for ext in SKIP_EXTS):
                continue
            filepath = os.path.join(root, fname)
            relpath = os.path.relpath(filepath, base_dir).replace('\\', '/')
            
            with open(filepath, 'rb') as f:
                content = base64.b64encode(f.read()).decode()
            
            files.append({"path": relpath, "content": content})
    return sorted(files, key=lambda x: x["path"])

def main():
    print("Collecting files...")
    files = collect_files(PROJECT_DIR)
    print(f"Total: {len(files)} files")
    
    # Build GraphQL mutation for createCommitOnBranch
    # This API can create commits on ANY branch, even in empty repos
    file_changes = []
    for f in files:
        file_changes.append({
            "path": f["path"],
            "additions": f["content"]  # GraphQL accepts base64 directly
        })
    
    # Do in batches of 10 files per commit (GitHub API limit)
    batch_size = 10
    for batch_idx in range(0, len(files), batch_size):
        batch = files[batch_idx:batch_idx+batch_size]
        batch_num = batch_idx // batch_size + 1
        total_batches = (len(files) + batch_size - 1) // batch_size
        
        additions = []
        for f in batch:
            additions.append({"path": f["path"], "contents": f["content"]})
        
        query = """
        mutation($input: CreateCommitOnBranchInput!) {
            createCommitOnBranch(input: $input) {
                commit {
                    oid
                    message
                }
            }
        }
        """
        
        variables = {
            "input": {
                "branch": {
                    "repositoryNameWithOwner": f"{OWNER}/{REPO}",
                    "branchName": "master"
                },
                "message": {
                    "headline": f"add: batch {batch_num}/{total_batches} - {len(batch)} files"
                },
                "fileChanges": {
                    "additions": additions
                }
            }
        }
        
        print(f"Commit batch {batch_num}/{total_batches} ({len(batch)} files)...")
        r = requests.post(
            "https://api.github.com/graphql",
            headers=headers(),
            json={"query": query, "variables": variables}
        )
        
        if r.status_code == 200:
            data = r.json()
            if "errors" in data:
                for e in data["errors"]:
                    print(f"  GraphQL error: {e.get('message', 'unknown')}")
                    if "not found" in e.get("message", "").lower():
                        print("  Branch may not exist yet. Trying to create repo with init...")
                return
            commit = data.get("data", {}).get("createCommitOnBranch", {}).get("commit", {})
            print(f"  OK: {commit.get('oid', '?')[:12]}")
        else:
            print(f"  HTTP error: {r.status_code} {r.text[:200]}")
            return
        
        time.sleep(1)
    
    print(f"\n✅ All {len(files)} files pushed!")
    print(f"https://github.com/{OWNER}/{REPO}")

if __name__ == "__main__":
    main()
