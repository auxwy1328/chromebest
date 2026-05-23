# -*- coding: utf-8 -*-
"""Fix cover image paths to match actual directory names (slug-based)"""
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
        
        # Extract front matter
        fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if not fm_match:
            continue
        fm = fm_match.group(1)
        
        # Find images: ["/images/xxx/cover.jpg"]
        img_match = re.search(r'images:\s*\[([^\]]+)\]', fm)
        if not img_match:
            continue
        
        img_path = img_match.group(1).strip().strip('"').strip("'")
        
        # Extract current image directory
        # e.g. /images/plugins/chrome-password-manager/cover.jpg
        parts = img_path.split('/')
        if len(parts) < 3:
            continue
        
        current_img_dir = parts[2]  # e.g. "chrome-password-manager"
        expected_img_dir = slug  # e.g. "chrome-password-manager-comparison"
        
        if current_img_dir != expected_img_dir:
            # Check if actual file exists at correct path
            actual_dir = os.path.join(STATIC_IMG_DIR, section, expected_img_dir)
            if os.path.isdir(actual_dir):
                # Fix the path
                old_path = f"/images/{section}/{current_img_dir}"
                new_path = f"/images/{section}/{expected_img_dir}"
                new_content = content.replace(old_path, new_path)
                
                if new_content != content:
                    with open(fpath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"FIX: {section}/{slug}: {old_path} -> {new_path}")
                    fixed += 1
            else:
                print(f"SKIP: {section}/{slug}: dir {actual_dir} not found")

print(f"\nTotal fixed: {fixed}")
