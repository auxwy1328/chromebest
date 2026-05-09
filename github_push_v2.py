# -*- coding: utf-8 -*-
"""GitHub API push for EMPTY repo - use tree with base64 content"""
import requests, os, hashlib, base64

GITHUB_TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"
PROJECT_DIR = r"C:\Projects\chromebest"
BRANCH = "master"

SKIP_DIRS = {'.git', 'public', 'node_modules', '__pycache__', '.hugo_build.lock'}
SKIP_EXTS = {'.py'}

def get_token():
    with open(GITHUB_TOKEN_FILE, 'r') as f:
        return f.read().strip()

def headers():
    return {
        "Authorization": f"token {get_token()}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

def collect_files(base_dir):
    tree = []
    for root, dirs, filenames in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        for fname in filenames:
            if any(fname.endswith(ext) for ext in SKIP_EXTS):
                continue
            filepath = os.path.join(root, fname)
            relpath = os.path.relpath(filepath, base_dir).replace('\\', '/')
            
            with open(filepath, 'rb') as f:
                content = base64.b64encode(f.read()).decode()
            
            tree.append({
                "path": relpath,
                "mode": "100644",
                "type": "blob",
                "content": content
            })
    return sorted(tree, key=lambda x: x["path"])

def main():
    print("Collecting files (excluding .py scripts and build artifacts)...")
    tree = collect_files(PROJECT_DIR)
    print(f"Total files: {len(tree)}")
    total_bytes = sum(len(t["content"]) for t in tree)
    print(f"Total base64 size: {total_bytes // 1024 // 1024}MB")
    
    # For empty repos: create an initial commit with empty tree first
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}",
        headers=headers()
    )
    
    is_empty = r.status_code != 200
    
    if is_empty:
        print("Repo is empty. Creating initial commit first...")
        # Create an empty tree
        r = requests.post(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees",
            headers=headers(),
            json={"tree": []}
        )
        resp = r.json()
        if "sha" not in resp:
            print(f"Empty tree failed: {r.status_code} {r.text[:200]}")
            return
        empty_tree_sha = resp["sha"]
        
        # Create initial commit
        r = requests.post(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
            headers=headers(),
            json={"message": "initial commit", "tree": empty_tree_sha}
        )
        init_commit_sha = r.json()["sha"]
        
        # Create ref
        r = requests.put(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
            headers=headers(),
            json={"sha": init_commit_sha}
        )
        if r.status_code in (200, 201):
            print("Initial commit created")
        else:
            print(f"Failed to create initial commit: {r.text[:200]}")
            return
    
    print("Step 1: Creating blobs...")
    blob_tree = []
    for i, item in enumerate(tree):
        r = requests.post(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs",
            headers=headers(),
            json={"content": item["content"], "encoding": "base64"}
        )
        if r.status_code == 201:
            blob_tree.append({
                "path": item["path"],
                "mode": "100644",
                "type": "blob",
                "sha": r.json()["sha"]
            })
            if (i + 1) % 10 == 0:
                print(f"  {i+1}/{len(tree)}")
        else:
            print(f"  FAIL [{item['path']}]: {r.status_code}")
            # Try creating tree first then if empty repo issue
            return
    
    print(f"All {len(blob_tree)} blobs created")
    
    print("Step 2: Creating tree...")
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees",
        headers=headers(),
        json={"tree": blob_tree}
    )
    if r.status_code != 201:
        print(f"Tree failed: {r.text[:300]}")
        return
    tree_sha = r.json()["sha"]
    print(f"Tree SHA: {tree_sha}")
    
    print("Step 3: Creating commit...")
    commit_body = {
        "message": "init: chromebest.com - 25 articles, images, favicon, Hugo templates",
        "tree": tree_sha,
        "parents": [init_commit_sha] if is_empty else []
    }
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
        headers=headers(),
        json=commit_body
    )
    if r.status_code != 201:
        print(f"Commit failed: {r.text[:300]}")
        return
    commit_sha = r.json()["sha"]
    print(f"Commit: {commit_sha}")
    
    print("Step 4: Creating/updating ref...")
    r = requests.put(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
        headers=headers(),
        json={"sha": commit_sha}
    )
    if r.status_code == 201:
        print(f"\n✅ Push complete!")
        print(f"https://github.com/{OWNER}/{REPO}")
    elif r.status_code == 200:
        print(f"\n✅ Ref updated!")
        print(f"https://github.com/{OWNER}/{REPO}")
    else:
        print(f"Ref failed: {r.status_code} {r.text[:300]}")

if __name__ == "__main__":
    main()
