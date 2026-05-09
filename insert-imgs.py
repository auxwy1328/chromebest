import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
articles = [
    ('content/tips/chrome-clear-cache.md', 'tips/chrome-clear-cache'),
    ('content/tips/chrome-extensions-not-working.md', 'tips/chrome-extensions-not-working'),
]
for f, slug in articles:
    with open(f, 'r', encoding='utf-8') as fh:
        text = fh.read()
    if 'body1.jpg' in text:
        print('SKIP (has body1): ' + os.path.basename(f))
        continue
    img_line = '\n![' + os.path.basename(f).replace('.md','') + '](/images/' + slug + '/body1.jpg)\n'
    m = re.search(r'\n## ', text)
    if m:
        text = text[:m.start()] + img_line + text[m.start():]
        with open(f, 'w', encoding='utf-8') as fh:
            fh.write(text)
        print('OK: ' + os.path.basename(f))
