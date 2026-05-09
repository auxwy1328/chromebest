# -*- coding: utf-8 -*-
"""Quick push single file fix to GitHub API"""
import requests, base64, json

GITHUB_TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"

def get_token():
    with open(GITHUB_TOKEN_FILE, 'r') as f:
        return f.read().strip()

def headers():
    return {
        "Authorization": f"token {get_token()}",
        "Accept": "application/vnd.github+json",
        "Content-Type": "application/json"
    }

# Read hugo.toml
with open(r"C:\Projects\chromebest\hugo.toml", 'r', encoding='utf-8') as f:
    content = base64.b64encode(f.read().encode('utf-8')).decode()

# Get current file SHA
r = requests.get(
    f"https://api.github.com/repos/{OWNER}/{REPO}/contents/hugo.toml",
    headers=headers()
)
sha = r.json()["sha"]

# Update file
r = requests.put(
    f"https://api.github.com/repos/{OWNER}/{REPO}/contents/hugo.toml",
    headers=headers(),
    json={
        "message": "fix: paginate → pagination.pagerSize for Hugo 0.147+",
        "content": content,
        "sha": sha,
        "branch": "master"
    }
)
if r.status_code == 200:
    print(f"✅ Updated hugo.toml")
    print(f"Commit: {r.json()['commit']['sha'][:12]}")
else:
    print(f"FAIL: {r.status_code} {r.text[:200]}")
