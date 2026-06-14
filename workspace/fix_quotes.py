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

remaining = sum(1 for ch in content if ch in bad_chars)
print(f'Remaining CN quotes: {remaining}')

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print('Done replacing quotes')
