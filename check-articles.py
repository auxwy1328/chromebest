import re, os, sys
sys.stdout.reconfigure(encoding='utf-8')
base = r'C:\Projects\chromebest'
articles = [
    ('content/tips/chrome-clear-cache.md', 'tips/chrome-clear-cache'),
    ('content/tips/chrome-extensions-not-working.md', 'tips/chrome-extensions-not-working'),
]
all_pass = True
for f, slug in articles:
    path = os.path.join(base, f)
    with open(path, 'r', encoding='utf-8') as fh:
        text = fh.read()
    body = re.sub(r'^---.*?---', '', text, flags=re.DOTALL).strip()
    chars = len(re.sub(r'\s+', '', body))
    faq_count = len(re.findall(r'- q:', text))
    links = [l for l in re.findall(r'\[.*?\]\(/.*?\)', body) if '/images/' not in l]
    has_body_img = bool(re.search(r'!\[.*?\]\(/images/', body))
    cover_path = os.path.join(base, 'static', 'images', slug, 'cover.jpg')
    body_path = os.path.join(base, 'static', 'images', slug, 'body1.jpg')
    cover_exists = os.path.exists(cover_path)
    body_exists = os.path.exists(body_path)
    fm_images = re.search(r'images:\s*\["([^"]+)"\]', text)
    fm_path_ok = False
    if fm_images:
        fm_img = fm_images.group(1)
        fm_path_ok = os.path.exists(os.path.join(base, 'static', fm_img.lstrip('/')))

    print('=== ' + os.path.basename(f) + ' ===')
    checks = [
        ('1. Chars >= 2500', chars >= 2500, str(chars)),
        ('2. FAQ >= 5', faq_count >= 5, str(faq_count)),
        ('3. Internal links 3-5', 3 <= len(links) <= 5, str(len(links))),
        ('4. Cover image exists', cover_exists, cover_path),
        ('5. Body image inserted', has_body_img, 'yes' if has_body_img else 'NO'),
        ('6. Image path consistent', fm_path_ok and cover_exists, 'fm=' + str(fm_path_ok) + ' file=' + str(cover_exists)),
    ]
    for name, passed, detail in checks:
        status = 'PASS' if passed else 'FAIL'
        if not passed: all_pass = False
        print('  ' + status + ' | ' + name + ' (' + detail + ')')
    print()

print('OVERALL: ' + ('ALL PASS' if all_pass else 'HAS FAIL - FIX BEFORE PUBLISH'))
