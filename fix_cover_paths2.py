# -*- coding: utf-8 -*-
"""Fix cover image paths: use slug-based directory names"""
import os, re

CONTENT_DIR = r"C:\Projects\chromebest\content"
STATIC_IMG_DIR = r"C:\Projects\chromebest\static\images"

fixed = 0
for root, dirs, files in os.walk(CONTENT_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        section = os.path.basename(root)
        slug = fname.replace('.md', '')
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            continue
        
        fm = fm_match.group(1)
        img_match = re.search(r'images:\s*\["([^"]+)"\]', fm)
        if not img_match:
            continue
        
        old_img_path = img_match.group(1)
        # Extract what directory FM currently references
        # e.g. /images/compare/chrome-cross-platform/cover.jpg -> chrome-cross-platform
        parts = old_img_path.split('/')
        if len(parts) < 4:
            continue
        
        old_dir = parts[2]  # chrome-cross-platform
        
        # Build correct path using slug
        correct_path = f"/images/{section}/{slug}/cover.jpg"
        
        if old_img_path != correct_path:
            # Verify actual file exists
            actual_file = os.path.join(STATIC_IMG_DIR, section, slug, "cover.jpg")
            if os.path.exists(actual_file):
                new_content = content.replace(old_img_path, correct_path)
                with open(fpath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"FIX: {slug}: {old_img_path} -> {correct_path}")
                fixed += 1
            else:
                print(f"MISSING FILE: {slug}: {actual_file}")

print(f"\nTotal fixed: {fixed}")
