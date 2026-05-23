# -*- coding: utf-8 -*-
import re, os

base = r'C:\Projects\chromebest\content'

articles = [
    ('tips', 'chrome-update-failed-fix.md', '第23篇'),
    ('tips', 'chrome-sync-settings-guide.md', '第24篇'),
    ('tips', 'chrome-set-default-browser-guide.md', '第25篇'),
]

for section, filename, label in articles:
    path = os.path.join(base, section, filename)
    text = open(path, 'r', encoding='utf-8').read()
    
    # Check front matter
    parts = text.split('---')
    if len(parts) < 3:
        print(f'{label} {filename}: FAIL - no front matter')
        continue
    
    fm = parts[1]
    body = '---'.join(parts[2:])
    
    title = re.search(r'title:\s*"(.+?)"', fm)
    date = re.search(r'date:', fm)
    slug = re.search(r'slug:', fm)
    desc = re.search(r'description:', fm)
    images = re.search(r'images:', fm)
    categories = re.search(r'categories:', fm)
    tags = re.search(r'tags:', fm)
    
    chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', body))
    h2_count = len(re.findall(r'^## ', body, re.MULTILINE))
    faq_count = len(re.findall(r'^### ', body, re.MULTILINE))
    
    checks = []
    if title: checks.append('title')
    if date: checks.append('date')
    if slug: checks.append('slug')
    if desc: checks.append('desc')
    if images: checks.append('images')
    if categories: checks.append('categories')
    if tags: checks.append('tags')
    if chinese_chars >= 2500: checks.append('2500+chars')
    if h2_count >= 3: checks.append(f'{h2_count}xH2')
    if faq_count >= 5: checks.append(f'{faq_count}xFAQ')
    
    status = 'PASS' if len(checks) >= 9 else 'FAIL'
    print(f'{label} {filename}: {status} | {chinese_chars}chars | {h2_count}H2 | {faq_count}FAQ | {", ".join(checks)}')
