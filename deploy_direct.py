# -*- coding: utf-8 -*-
"""Direct Cloudflare Pages deployment via API (bypasses wrangler User permission)"""
import requests, os, zipfile, io, hashlib, sys

TOKEN_FILE = r"C:\Users\15645\Desktop\cfToken.txt"
ACCOUNT_ID = "b8faf46813646ff3625ffdbac9403fe8"
PROJECT_NAME = "chromebest"
PUBLIC_DIR = r"C:\Projects\chromebest\public"

def get_token():
    with open(TOKEN_FILE, 'r') as f:
        return f.read().strip()

def create_zip(directory):
    """Create zip of all files in directory"""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(directory):
            for file in files:
                filepath = os.path.join(root, file)
                arcname = os.path.relpath(filepath, directory).replace('\\', '/')
                zf.write(filepath, arcname)
    buf.seek(0)
    return buf

def check_project(token):
    """Check if Pages project exists"""
    r = requests.get(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}",
        headers={"Authorization": f"Bearer {token}"}
    )
    data = r.json()
    if data.get("success"):
        print(f"Project '{PROJECT_NAME}' exists: {data['result'].get('subdomain', 'N/A')}.pages.dev")
        return True
    elif data.get("errors"):
        for e in data["errors"]:
            print(f"API Error: {e.get('message', 'unknown')}")
        return False
    return False

def create_project(token):
    """Create Pages project"""
    r = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json={"name": PROJECT_NAME, "production_branch": "main"}
    )
    data = r.json()
    if data.get("success"):
        print(f"Created project '{PROJECT_NAME}'")
        return True
    elif data.get("errors"):
        for e in data["errors"]:
            print(f"Create error: {e.get('message', 'unknown')}")
    return False

def upload_deploy(token, zip_buf):
    """Upload direct upload deployment"""
    # Step 1: Get upload URL using direct_upload endpoint
    r = requests.post(
        f"https://api.cloudflare.com/client/v4/accounts/{ACCOUNT_ID}/pages/projects/{PROJECT_NAME}/deployments",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        json={
            "branch": "main"
        }
    )
    data = r.json()
    
    if not data.get("success"):
        for e in data.get("errors", []):
            print(f"Deploy init error: {e.get('message', 'unknown')}")
        return None
    
    upload_info = data["result"]
    jwt = upload_info.get("jwt")
    upload_url = upload_info.get("upload_url")
    
    if not jwt or not upload_url:
        print(f"No upload URL returned. Response: {data}")
        return None
    
    print(f"Got upload URL, uploading {len(zip_buf.getvalue())//1024}KB...")
    
    # Step 2: Upload files using multipart form
    files = {}
    zip_buf.seek(0)
    with zipfile.ZipFile(zip_buf, 'r') as zf:
        for name in zf.namelist():
            files[name] = (name, zf.read(name))
    
    r = requests.post(
        upload_url,
        headers={"Authorization": f"Bearer {jwt}"},
        files=files
    )
    
    if r.status_code == 200:
        result = r.json()
        deployment_id = result.get("id", "unknown")
        url = result.get("url", "unknown")
        print(f"Deployed! URL: {url}")
        print(f"Deployment ID: {deployment_id}")
        return url
    else:
        print(f"Upload failed: {r.status_code} {r.text[:500]}")
        return None

def main():
    token = get_token()
    
    # Check or create project
    if not check_project(token):
        print("Project not found, creating...")
        if not create_project(token):
            print("Failed to create project. Check token permissions.")
            return
    
    # Create zip
    print("Creating zip of public directory...")
    zip_buf = create_zip(PUBLIC_DIR)
    print(f"Zip size: {len(zip_buf.getvalue())//1024}KB")
    
    # Deploy
    url = upload_deploy(token, zip_buf)
    if url:
        print(f"\n✅ Deployment complete!")
        print(f"Preview: {url}")

if __name__ == "__main__":
    main()
