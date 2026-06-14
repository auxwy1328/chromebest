import re, os

path = r'C:\Projects\chromebest\content\tips\chrome-default-browser.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Split front matter and body
parts = content.split('---', 2)
body = parts[2] if len(parts) >= 3 else content

# Word count (Chinese chars + English words)
cn_chars = len(re.findall(r'[\u4e00-\u9fff]', body))
en_words = len(re.findall(r'[a-zA-Z]+', body))
total_words = cn_chars + en_words
print(f'Words: {total_words} (CN: {cn_chars}, EN: {en_words})')
print(f'Words >= 5000: {"PASS" if total_words >= 5000 else "FAIL"}')

# Home links (links to /)
home_links = re.findall(r'\[([^\]]+)\]\(\s*/\s*\)', body)
print(f'Home links ({len(home_links)}): {home_links}')
print(f'Home links >= 3: {"PASS" if len(home_links) >= 3 else "FAIL"}')

# Internal links
valid_paths = ['/tips/chrome-clear-cache/', '/tips/chrome-search-engine-change/', '/tips/chrome-proxy-settings/', '/plugins/chrome-essential-extensions/', '/tips/chrome-page-not-loading/', '/tips/chrome-update-failed/', '/download/chrome-offline-installer/', '/compare/chrome-vs-edge-2026/', '/tips/chrome-notification-settings/', '/tips/chrome-tab-groups/', '/plugins/chrome-ad-blocker-extension-recommendation/', '/plugins/chrome-screenshot-extensions/', '/tips/chrome-hardware-acceleration/']
internal_links = []
for p in valid_paths:
    matches = re.findall(rf'\[[^\]]*\]\(\s*{re.escape(p)}\s*\)', body)
    if matches:
        internal_links.append((p, matches[0]))
print(f'Internal links ({len(internal_links)}):')
for p, m in internal_links:
    print(f'  {m}')
print(f'Internal links >= 3: {"PASS" if len(internal_links) >= 3 else "FAIL"}')

# Images in body
body_images = re.findall(r'!\[[^\]]*\]\(\s*/images/[^\)]+\)', body)
print(f'Body images ({len(body_images)}):')
for img in body_images:
    print(f'  {img}')

# Image files in static dir
img_dir = r'C:\Projects\chromebest\static\images\tips\chrome-default-browser'
img_files = [f for f in os.listdir(img_dir) if f.endswith(('.jpg', '.png', '.webp'))] if os.path.isdir(img_dir) else []
print(f'Image files in static: {img_files}')
print(f'Images >= 5: {"PASS" if len(img_files) >= 5 else "FAIL"}')

# FAQ count
faq_matches = re.findall(r'- question:', content)
print(f'FAQ count: {len(faq_matches)}')
print(f'FAQ >= 5: {"PASS" if len(faq_matches) >= 5 else "FAIL"}')

# Check no Chinese quotes
cn_quotes = re.findall(r'[\u201c\u201d]', content)
print(f'Chinese quotes found: {len(cn_quotes)}')

# Check no emoji in headings
headings = re.findall(r'^#+\s+.+$', body, re.MULTILINE)
emoji_headings = [h for h in headings if re.search(r'[\U0001f300-\U0001f9ff]', h)]
print(f'Emoji in headings: {len(emoji_headings)}')
