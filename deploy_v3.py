# -*- coding: utf-8 -*-
"""Cloudflare Pages Direct Upload using PUT with JWT"""
import requests, os, zipfile, io, hashlib, base64, json

TOKEN_FILE = r"C:\Users\15645\Desktop\cfToken.txt"
ACCOUNT_ID = "b8faf46813646ff3625ffdbac9403fe8"
PROJECT_NAME = "chromebest"
PUBLIC_DIR = r"C:\Projects\chromebest\public"

def get_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

def build_manifest_and_files(directory):
    """Build manifest (with hashes only) and collect files"""
    manifest = []
    files_map = {}
    
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            relpath = os.path.relpath(filepath, directory).replace('\\', '/')
            
            with open(filepath, 'rb') as f:
                content = f.read()
            
            file_hash = hashlib.sha256(content).hexdigest()
            manifest.append({
                "filepath": f"/{relpath}",
                "hash": file_hash
            })
            files_map[f"/{relpath}"] = content
    
    return manifest, files_map

def main():
    token = get_token()
    
    print("Building manifest...")
    manifest, files_map = build_manifest_and_files(PUBLIC_DIR)
    print(f"Total files: {len(manifest)}")
    
    # Step 1: Request upload JWT
    print("Requesting upload URL...")
    r = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"manifest": manifest, "branch": "main"}
    )
    
    data = r.json()
    print(f"Response success: {data.get('success')}")
    
    if not data.get("success"):
        for e in data.get("errors", []):
            print(f"Error: {e.get('message', 'unknown')}")
        return
    
    jwt = data["result"]["jwt"]
    upload_url = data["result"]["upload_url"]
    print(f"Got JWT, upload URL: {upload_url}")
    
    # Step 2: Upload files via multipart PUT
    print("Uploading files...")
    files_list = []
    for filepath, content in files_map.items():
        files_list.append(("file", (filepath, content)))
    
    r = requests.put(upload_url, headers={"Authorization": f"Bearer {jwt}"}, files=files_list)
    
    if r.status_code == 200:
        result = r.json()
        print(f"\n✅ Deployment complete!")
        print(f"URL: {result.get('url', 'unknown')}")
    else:
        print(f"Upload failed: {r.status_code}")
        print(r.text[:500])

if __name__ == "__main__":
    main()
