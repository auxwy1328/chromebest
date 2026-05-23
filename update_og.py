# -*- coding: utf-8 -*-
"""Update front matter og_image to point to og.jpg for all articles"""
import os, re

CONTENT_DIR = r"C:\Projects\chromebest\content"
STATIC_IMG_DIR = r"C:\Projects\chromebest\static\images"

updated = 0
for root, dirs, files in os.walk(CONTENT_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        section = os.path.basename(root)
        slug = fname.replace('.md', '')
        
        # Check if og.jpg exists
        og_file = os.path.join(STATIC_IMG_DIR, section, slug, "og.jpg")
        if not os.path.exists(og_file):
            continue
        
        og_path = f"/images/{section}/{slug}/og.jpg"
        
        with open(fpath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Update or add og_image
        if 'og_image:' in content:
            # Replace existing
            new_content = re.sub(r'^og_image:.*$', f'og_image: "{og_path}"', content, flags=re.MULTILINE)
        else:
            # Add after images line
            new_content = content.replace(
                f'images: ["/images/{section}/{slug}/cover.jpg"]',
                f'images: ["/images/{section}/{slug}/cover.jpg"]\nog_image: "{og_path}"'
            )
        
        if new_content != content:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated += 1
            print(f"Updated: {section}/{slug}")

print(f"\nTotal updated: {updated}")
