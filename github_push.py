# -*- coding: utf-8 -*-
"""GitHub API push: push all chromebest files to auxwy1328/chromebest repo"""
import requests, os, hashlib, base64, json

GITHUB_TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"
PROJECT_DIR = r"C:\Projects\chromebest"
BRANCH = "master"

# Files to skip
SKIP_DIRS = {'.git', 'public', 'node_modules', '__pycache__', 'resources', '.hugo_build.lock'}
SKIP_FILES = {'.DS_Store', 'Thumbs.db'}

def get_token():
    with open(GITHUB_TOKEN_FILE, 'r') as f:
        return f.read().strip()

def get_headers():
    return {
        "Authorization": f"token {get_token()}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

def get_sha(owner, repo, path, branch):
    """Get SHA of a file in the repo"""
    r = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/contents/{path}",
        headers=get_headers(),
        params={"ref": branch}
    )
    if r.status_code == 200:
        return r.json()["sha"]
    return None

def get_main_tree(owner, repo, branch):
    """Get the tree SHA of the latest commit on branch"""
    r = requests.get(
        f"https://api.github.com/repos/{owner}/{repo}/git/ref/heads/{branch}",
        headers=get_headers()
    )
    if r.status_code == 200:
        data = r.json()
        commit_sha = data["object"]["sha"]
        # Get tree SHA from commit
        r2 = requests.get(
            f"https://api.github.com/repos/{owner}/{repo}/git/commits/{commit_sha}",
            headers=get_headers()
        )
        if r2.status_code == 200:
            return r2.json()["tree"]["sha"], commit_sha
    return None, None

def collect_files(base_dir):
    """Collect all files to push"""
    files = []
    for root, dirs, filenames in os.walk(base_dir):
        # Skip directories
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS and not d.startswith('.')]
        
        for fname in filenames:
            if fname in SKIP_FILES:
                continue
            filepath = os.path.join(root, fname)
            relpath = os.path.relpath(filepath, base_dir).replace('\\', '/')
            files.append((relpath, filepath))
    
    return sorted(files)

def main():
    # Collect files
    print("Collecting files...")
    files = collect_files(PROJECT_DIR)
    print(f"Total files: {len(files)}")
    
    # Create blobs
    print("Creating blobs...")
    blobs = []
    for relpath, filepath in files:
        with open(filepath, 'rb') as f:
            content = base64.b64encode(f.read()).decode()
        
        r = requests.post(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs",
            headers=get_headers(),
            json={"content": content, "encoding": "base64"}
        )
        if r.status_code == 201:
            blob_sha = r.json()["sha"]
            blobs.append({
                "path": relpath,
                "mode": "100644",
                "type": "blob",
                "sha": blob_sha
            })
            if len(blobs) % 20 == 0:
                print(f"  {len(blobs)}/{len(files)} blobs created")
        else:
            print(f"  FAIL: {relpath} - {r.status_code} {r.text[:100]}")
    
    print(f"All {len(blobs)} blobs created")
    
    # Create tree
    print("Creating tree...")
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees",
        headers=get_headers(),
        json={"base_tree": None, "tree": blobs}
    )
    if r.status_code != 201:
        print(f"Tree creation failed: {r.text[:300]}")
        return
    
    tree_sha = r.json()["sha"]
    print(f"Tree SHA: {tree_sha}")
    
    # Create commit
    print("Creating commit...")
    # Get parent commit
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}",
        headers=get_headers()
    )
    
    commit_body = {
        "message": "add: 25 articles + images + favicon - initial full content",
        "tree": tree_sha
    }
    
    if r.status_code == 200:
        parent_sha = r.json()["object"]["sha"]
        commit_body["parents"] = [parent_sha]
        print(f"Parent: {parent_sha}")
    
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
        headers=get_headers(),
        json=commit_body
    )
    if r.status_code != 201:
        print(f"Commit creation failed: {r.text[:300]}")
        return
    
    commit_sha = r.json()["sha"]
    print(f"Commit SHA: {commit_sha}")
    
    # Update ref
    print("Updating ref...")
    r = requests.patch(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
        headers=get_headers(),
        json={"sha": commit_sha}
    )
    if r.status_code == 200:
        print(f"\n✅ Push complete!")
        print(f"Repo: https://github.com/{OWNER}/{REPO}")
        print(f"Commit: {commit_sha}")
    else:
        print(f"Ref update failed: {r.text[:300]}")

if __name__ == "__main__":
    main()
