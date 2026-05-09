# -*- coding: utf-8 -*-
"""Fix front matter image paths - add section subdirectory"""
import os, re, base64, requests

CONTENT_DIR = r"C:\Projects\chromebest\content"
GITHUB_TOKEN_FILE = r"C:\Users\15645\Desktop\githubToken.txt"
OWNER = "auxwy1328"
REPO = "chromebest"

def get_token():
    with open(GITHUB_TOKEN_FILE, 'r') as f:
        return f.read().strip()

# Files to fix: old articles with wrong image paths
# The image paths in front matter are like /images/chrome-xxx/cover.jpg
# But actual files are in /images/{section}/chrome-xxx/cover.jpg
# New articles (23-25) already have correct paths

fixes = []
for root, dirs, files in os.walk(CONTENT_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        section = os.path.basename(root)
        relpath = f"{section}/{fname}"
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Find images: [...] in front matter
        fm_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
        if not fm_match:
            continue
        
        fm = fm_match.group(1)
        
        # Find all image paths
        img_matches = re.findall(r'/images/(chrome-[^/]+)/', fm)
        if not img_matches:
            continue
        
        # Check if section is already in path
        if f'/images/{section}/' in fm:
            continue
        
        # Fix: add section to image paths
        new_fm = fm.replace(f'/images/chrome-', f'/images/{section}/chrome-')
        new_content = content.replace(fm, new_fm)
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            fixes.append(relpath)
            print(f"Fixed: {relpath}")

print(f"\nTotal fixed: {len(fixes)}")
