import re

path = r'C:\Projects\chromebest\content\tips\chrome-save-password.md'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

bad_chars = '\u201c\u201d\u300c\u300d\u300e\u300f'
new_content = []
for ch in content:
    if ch in bad_chars:
        new_content.append('"')
    else:
        new_content.append(ch)
content = ''.join(new_content)

# Word count
chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', content))
english_words = len(re.findall(r'[a-zA-Z]+', content))
total = chinese_chars + english_words
print(f'Chinese chars: {chinese_chars}')
print(f'English words: {english_words}')
print(f'Total word count: {total}')
print(f'Word count >= 5000: {"PASS" if total >= 5000 else "FAIL"}')

# IMG markers
imgs = re.findall(r'<!-- IMG:.*?-->', content)
print(f'IMG markers: {len(imgs)} (need >= 5): {"PASS" if len(imgs) >= 5 else "FAIL"}')

# FAQ
faqs = re.findall(r'question:', content)
print(f'FAQ count: {len(faqs)} (need >= 5): {"PASS" if len(faqs) >= 5 else "FAIL"}')

# Homepage links
home_links = re.findall(r'\]\(\s*/\s*\)', content)
print(f'Homepage links: {len(home_links)} (need >= 3): {"PASS" if len(home_links) >= 3 else "FAIL"}')

# Internal links
internal_links = re.findall(r'\]\(\s*/[^)]+\)', content)
print(f'Internal links (total): {len(internal_links)} (need >= 3): {"PASS" if len(internal_links) >= 3 else "FAIL"}')

# Chinese quotes
cn_quotes = sum(1 for ch in content if ch in bad_chars)
print(f'Chinese quotes: {cn_quotes} (need = 0): {"PASS" if cn_quotes == 0 else "FAIL"}')

# Emoji in headings
headings = re.findall(r'^##.*$', content, re.MULTILINE)
emoji_headings = [h for h in headings if re.search(r'[\U0001f300-\U0001f9ff]', h)]
print(f'Emoji in headings: {len(emoji_headings)} (need = 0): {"PASS" if len(emoji_headings) == 0 else "FAIL"}')

# Print all links for review
print('\n--- All links ---')
for m in re.finditer(r'\]\(([^)]+)\)', content):
    print(f'  {m.group(1)}')
