import os, re, sys
sys.stdout.reconfigure(encoding='utf-8')
for root, dirs, files in os.walk('content'):
    for f in sorted(files):
        if f == '_index.md': continue
        path = os.path.join(root, f)
        with open(path, 'r', encoding='utf-8') as fh:
            text = fh.read()
        m = re.search(r'title:\s*"([^"]+)"', text)
        if not m: m = re.search(r'title:\s*(.+)', text)
        title = m.group(1) if m else f
        sec = os.path.basename(root)
        print(sec + ' | ' + title)
