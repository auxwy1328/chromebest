# -*- coding: utf-8 -*-
"""Initialize empty GitHub repo by creating first file via Contents API, then push all files"""
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
            files.append((relpath, content))
    return sorted(files, key=lambda x: x[0])

def main():
    print("Collecting files...")
    files = collect_files(PROJECT_DIR)
    print(f"Total: {len(files)} files")
    
    # Step 1: Initialize repo by creating first file via Contents API
    # Contents API PUT works on empty repos
    print("Initializing repo with first file...")
    first_path, first_content = files[0]
    r = requests.put(
        f"https://api.github.com/repos/{OWNER}/{REPO}/contents/{first_path}",
        headers=gh_headers(),
        json={
            "message": "init",
            "content": first_content,
            "branch": BRANCH
        }
    )
    if r.status_code == 201:
        print(f"Initialized! First file: {first_path}")
        parent_sha = r.json()["commit"]["sha"]
        remaining = files[1:]
    else:
        print(f"Init failed: {r.status_code} {r.text[:200]}")
        return
    
    # Step 2: Create blobs for remaining files
    print(f"Creating {len(remaining)} blobs...")
    blob_tree = []
    for i, (relpath, content) in enumerate(remaining):
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
            if (i + 1) % 10 == 0:
                print(f"  {i+1}/{len(remaining)}")
        else:
            print(f"  FAIL [{relpath}]: {r.status_code}")
            return
    
    print(f"All {len(blob_tree)} blobs created")
    
    # Also add the first file as blob to the tree
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs",
        headers=gh_headers(),
        json={"content": first_content, "encoding": "base64"}
    )
    first_blob_sha = r.json()["sha"]
    blob_tree.insert(0, {"path": first_path, "mode": "100644", "type": "blob", "sha": first_blob_sha})
    
    # Step 3: Create tree
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
    
    # Step 4: Create commit with parent
    print("Creating commit...")
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
        headers=gh_headers(),
        json={
            "message": "add: 25 articles + images + favicon + Hugo templates",
            "tree": tree_sha,
            "parents": [parent_sha]
        }
    )
    if r.status_code != 201:
        print(f"Commit failed: {r.text[:300]}")
        return
    commit_sha = r.json()["sha"]
    
    # Step 5: Update ref
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
