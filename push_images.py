# -*- coding: utf-8 -*-
"""Push all new images and updated MD files to GitHub via API"""
import requests, os, base64, time

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

def gh_headers():
    return {
        "Authorization": f"token {get_token()}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

def collect_changed_files(base_dir):
    """Collect all files"""
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
            files.append((relpath, content))
    return sorted(files, key=lambda x: x[0])

def main():
    print("Collecting files...")
    files = collect_changed_files(PROJECT_DIR)
    print(f"Total: {len(files)} files")
    
    # Get current commit SHA
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}",
        headers=gh_headers()
    )
    parent_sha = r.json()["object"]["sha"]
    print(f"Parent: {parent_sha[:12]}")
    
    # Create blobs
    print("Creating blobs...")
    blob_tree = []
    for i, (relpath, content) in enumerate(files):
        r = requests.post(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs",
            headers=gh_headers(),
            json={"content": content, "encoding": "base64"}
        )
        if r.status_code == 201:
            blob_tree.append({
                "path": relpath,
                "mode": "100644",
                "type": "blob",
                "sha": r.json()["sha"]
            })
            if (i + 1) % 20 == 0:
                print(f"  {i+1}/{len(files)}")
        else:
            print(f"  FAIL [{relpath}]: {r.status_code}")
            return
    
    print(f"All {len(blob_tree)} blobs created")
    
    # Create tree
    print("Creating tree...")
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees",
        headers=gh_headers(),
        json={"tree": blob_tree}
    )
    if r.status_code != 201:
        print(f"Tree failed: {r.text[:300]}")
        return
    tree_sha = r.json()["sha"]
    
    # Create commit
    print("Creating commit...")
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
        headers=gh_headers(),
        json={
            "message": "add: 88 article images (cover + body) for 22 articles",
            "tree": tree_sha,
            "parents": [parent_sha]
        }
    )
    if r.status_code != 201:
        print(f"Commit failed: {r.text[:300]}")
        return
    commit_sha = r.json()["sha"]
    
    # Update ref
    print("Updating ref...")
    r = requests.patch(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
        headers=gh_headers(),
        json={"sha": commit_sha}
    )
    if r.status_code == 200:
        print(f"\n✅ Push complete! {len(files)} files")
        print(f"https://github.com/{OWNER}/{REPO}")
    else:
        print(f"Ref failed: {r.text[:200]}")

if __name__ == "__main__":
    main()
