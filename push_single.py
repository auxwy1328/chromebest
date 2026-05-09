# -*- coding: utf-8 -*-
"""Push single file to GitHub via Contents API"""
import requests, base64

TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"

def get_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

# Read file
filepath = r"C:\Projects\chromebest\layouts\_default\single.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = base64.b64encode(f.read().encode('utf-8')).decode()

headers = {
    "Authorization": f"token {get_token()}",
    "Accept": "application/vnd.github+json",
    "Content-Type": "application/json"
}

# Get SHA
r = requests.get(f"https://api.github.com/repos/{OWNER}/{REPO}/contents/layouts/_default/single.html", headers=headers)
sha = r.json()["sha"]

# Update
r = requests.put(
    f"https://api.github.com/repos/{OWNER}/{REPO}/contents/layouts/_default/single.html",
    headers=headers,
    json={"message": "fix: simplify breadcrumb for Hugo 0.147 compat", "content": content, "sha": sha, "branch": "master"}
)
if r.status_code == 200:
    print(f"OK: {r.json()['commit']['sha'][:12]}")
else:
    print(f"FAIL: {r.status_code} {r.text[:200]}")
