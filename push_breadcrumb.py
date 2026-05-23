# -*- coding: utf-8 -*-
"""Push breadcrumb + CSS update to GitHub"""
import requests, base64, json

TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"
BRANCH = "master"
PROJECT_DIR = r"C:\Projects\chromebest"

FILES = [
    "layouts/_default/single.html",
    "static/css/style.css",
]

def get_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

def headers():
    return {
        "Authorization": f"token {get_token()}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

def main():
    # Get parent SHA
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}",
        headers=headers()
    )
    parent_sha = r.json()["object"]["sha"]
    
    # Create blobs
    blobs = []
    for relpath in FILES:
        filepath = os.path.join(PROJECT_DIR, relpath) if 'os' in dir() else None
        import os
        filepath = os.path.join(PROJECT_DIR, relpath)
        with open(filepath, 'rb') as f:
            content = base64.b64encode(f.read()).decode()
        
        r = requests.post(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs",
            headers=headers(),
            json={"content": content, "encoding": "base64"}
        )
        blobs.append({"path": relpath, "mode": "100644", "type": "blob", "sha": r.json()["sha"]})
        print(f"Blob: {relpath}")
    
    # Tree
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees",
        headers=headers(),
        json={"tree": blobs}
    )
    tree_sha = r.json()["sha"]
    
    # Commit
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
        headers=headers(),
        json={"message": "add: breadcrumb navigation on article pages", "tree": tree_sha, "parents": [parent_sha]}
    )
    commit_sha = r.json()["sha"]
    
    # Update ref
    r = requests.patch(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
        headers=headers(),
        json={"sha": commit_sha}
    )
    if r.status_code == 200:
        print(f"\n✅ Pushed: {commit_sha[:12]}")
    else:
        print(f"FAIL: {r.text[:200]}")

if __name__ == "__main__":
    main()
