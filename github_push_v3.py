# -*- coding: utf-8 -*-
"""Push to empty GitHub repo using Contents API (works with empty repos)"""
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

def headers():
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
    
    # Use Git Data API to create objects manually
    # Empty repo workaround: use low-level git object creation
    
    # First, create a tree with all file blobs embedded as content
    # GitHub allows creating blobs in empty repos via the API
    # The trick: POST to /git/blobs works even for empty repos
    
    # Actually, let me try the raw Git HTTP backend approach
    # Or simpler: use GitHub's "upload files" via the GraphQL API
    
    # Simplest approach: delete and recreate repo via API, using 
    # the "auto_init" parameter which creates an initial commit
    
    # Delete current empty repo
    print("Deleting empty repo to recreate with auto_init...")
    r = requests.delete(
        f"https://api.github.com/repos/{OWNER}/{REPO}",
        headers=headers()
    )
    if r.status_code == 204:
        print("Deleted")
        time.sleep(2)
    elif r.status_code == 403:
        print("Cannot delete - try manual approach instead")
        # Fallback: use GraphQL
    else:
        print(f"Delete result: {r.status_code}")
    
    # Recreate with auto_init
    r = requests.post(
        f"https://api.github.com/user/repos",
        headers=headers(),
        json={
            "name": REPO,
            "description": "Chrome浏览器指南 - ChromeBest",
            "private": False,
            "auto_init": True
        }
    )
    if r.status_code == 201:
        print(f"Recreated repo with auto_init")
    else:
        print(f"Recreate failed: {r.status_code} {r.text[:200]}")
        return
    
    time.sleep(2)
    
    # Now the repo has an initial commit, so we can push normally
    print("Creating blobs on initialized repo...")
    blob_tree = []
    for i, (relpath, content) in enumerate(files):
        r = requests.post(
            f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs",
            headers=headers(),
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
                print(f"  {i+1}/{len(files)}")
        else:
            print(f"  FAIL [{relpath}]: {r.status_code}")
            return
    
    print(f"All {len(blob_tree)} blobs created")
    
    # Create tree
    print("Creating tree...")
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees",
        headers=headers(),
        json={"tree": blob_tree}
    )
    if r.status_code != 201:
        print(f"Tree failed: {r.text[:300]}")
        return
    tree_sha = r.json()["sha"]
    
    # Get current commit SHA as parent
    r = requests.get(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}",
        headers=headers()
    )
    parent_sha = r.json()["object"]["sha"]
    
    # Create commit
    print("Creating commit...")
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
        headers=headers(),
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
    
    # Update ref
    print("Updating ref...")
    r = requests.patch(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
        headers=headers(),
        json={"sha": commit_sha}
    )
    if r.status_code == 200:
        print(f"\n✅ Push complete!")
        print(f"https://github.com/{OWNER}/{REPO}")
    else:
        print(f"Ref update failed: {r.text[:200]}")

if __name__ == "__main__":
    main()
