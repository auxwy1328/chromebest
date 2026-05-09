# -*- coding: utf-8 -*-
"""Remove duplicate image lines in all markdown files"""
import os, re

CONTENT_DIR = r"C:\Projects\chromebest\content"

fixed = 0
for root, dirs, files in os.walk(CONTENT_DIR):
    for fname in files:
        if not fname.endswith('.md'):
            continue
        fpath = os.path.join(root, fname)
        
        with open(fpath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        lines = text.split('\n')
        seen = set()
        new_lines = []
        has_dups = False
        
        for line in lines:
            # Check if this is an image line
            img_match = re.match(r'^!\[.*?\]\(.+?\)$', line.strip())
            if img_match:
                if line.strip() in seen:
                    has_dups = True
                    continue
                seen.add(line.strip())
            new_lines.append(line)
        
        if has_dups:
            with open(fpath, 'w', encoding='utf-8') as f:
                f.write('\n'.join(new_lines))
            fixed += 1
            print(f"Deduped: {os.path.basename(root)}/{fname}")

print(f"\nTotal deduped: {fixed}")
