# -*- coding: utf-8 -*-
"""Cloudflare Pages Direct Upload - correct manifest-based deployment"""
import requests, os, zipfile, io, hashlib, base64

TOKEN_FILE = r"C:\Users\15645\Desktop\cfToken.txt"
ACCOUNT_ID = "b8faf46813646ff3625ffdbac9403fe8"
PROJECT_NAME = "chromebest"
PUBLIC_DIR = r"C:\Projects\chromebest\public"

def get_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

def build_manifest(directory):
    """Build manifest from all files"""
    manifest = []
    base64_files = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, directory).replace('\\', '/')
            
            with open(filepath, 'rb') as f:
                content = f.read()
            
            file_hash = hashlib.sha256(content).hexdigest()
            b64 = base64.b64encode(content).decode('ascii')
            
            manifest.append({
                "filepath": f"/{relpath}",
                "hash": file_hash,
                "content": b64
            })
    
    return manifest

def main():
    token = get_token()
    
    print("Building manifest...")
    manifest = build_manifest(PUBLIC_DIR)
    print(f"Total files: {len(manifest)}")
    total_size = sum(len(m['content']) for m in manifest)
    print(f"Total base64 size: {total_size // 1024}KB")
    
    print("Uploading...")
    r = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "branch": "main",
            "manifest": manifest
        }
    )
    
    data = r.json()
    if data.get("success"):
        url = data["result"].get("url", "")
        print(f"\n✅ Deployment complete!")
        print(f"URL: {url}")
    else:
        for e in data.get("errors", []):
            print(f"Error: {e.get('message', 'unknown')}")
            if e.get("chain"):
                for ce in e["chain"]:
                    print(f"  Chain: {ce.get('message', 'unknown')}")

if __name__ == "__main__":
    main()
