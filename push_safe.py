# -*- coding: utf-8 -*-
"""Push single file update via GitHub Contents API (safe, doesn't replace tree)"""
import requests, base64, os

TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"
BRANCH = "master"
PROJECT_DIR = r"C:\Projects\chromebest"

def get_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

def headers():
    return {
        "Authorization": f"token {get_token()}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

# List of files to update: (relative_path, local_path)
files_to_update = [
    ("static/css/style.css", os.path.join(PROJECT_DIR, "static", "css", "style.css")),
]

# Step 1: Get parent SHA
r = requests.get(
    f"https://api.github.com/repos/{OWNER}/{REPO}/git/ref/heads/{BRANCH}",
    headers=headers()
)
parent_sha = r.json()["object"]["sha"]
print(f"Parent: {parent_sha[:12]}")

# Step 2: Create blobs + tree with ALL files (safe approach)
import glob
all_files = []
for root, dirs, filenames in os.walk(PROJECT_DIR):
    dirs[:] = [d for d in dirs if d not in {'.git', 'public', 'node_modules', '__pycache__', '.hugo_build.lock'} and not d.startswith('.')]
    for fname in filenames:
        if fname.endswith('.py'):
            continue
        fpath = os.path.join(root, fname)
        relpath = os.path.relpath(fpath, PROJECT_DIR).replace('\\', '/')
        all_files.append((relpath, fpath))

all_files.sort(key=lambda x: x[0])
print(f"Total files: {len(all_files)}")

# Create blobs for ALL files
print("Creating blobs...")
blob_tree = []
for i, (relpath, fpath) in enumerate(all_files):
    with open(fpath, 'rb') as f:
        content = base64.b64encode(f.read()).decode()
    r = requests.post(
        f"https://api.github.com/repos/{OWNER}/{REPO}/git/blobs",
        headers=headers(),
        json={"content": content, "encoding": "base64"}
    )
    if r.status_code == 201:
        blob_tree.append({"path": relpath, "mode": "100644", "type": "blob", "sha": r.json()["sha"]})
    else:
        print(f"  FAIL [{relpath}]: {r.status_code}")
        exit(1)
    if (i + 1) % 30 == 0:
        print(f"  {i+1}/{len(all_files)}")
print(f"All {len(blob_tree)} blobs created")

# Step 3: Create tree
r = requests.post(
    f"https://api.github.com/repos/{OWNER}/{REPO}/git/trees",
    headers=headers(),
    json={"tree": blob_tree}
)
tree_sha = r.json()["sha"]

# Step 4: Create commit
r = requests.post(
    f"https://api.github.com/repos/{OWNER}/{REPO}/git/commits",
    headers=headers(),
    json={"message": "fix: remove sidebar padding-top, align with breadcrumb", "tree": tree_sha, "parents": [parent_sha]}
)
commit_sha = r.json()["sha"]

# Step 5: Update ref
r = requests.patch(
    f"https://api.github.com/repos/{OWNER}/{REPO}/git/refs/heads/{BRANCH}",
    headers=headers(),
    json={"sha": commit_sha}
)
if r.status_code == 200:
    print(f"\n✅ Pushed: {commit_sha[:12]}")
else:
    print(f"FAIL: {r.text[:200]}")
