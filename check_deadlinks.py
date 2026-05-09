# -*- coding: utf-8 -*-
"""Check all sitemap URLs for dead links (404)"""
import requests, time

SITEMAP_URL = "https://chromebest.com/sitemap.xml"
headers = {"User-Agent": "Mozilla/5.0 (compatible; SiteChecker/1.0)"}

# Extract URLs from sitemap
r = requests.get(SITEMAP_URL, timeout=15, headers=headers)
import re
urls = re.findall(r'<loc>([^<]+)</loc>', r.text)
print(f"Sitemap URLs: {len(urls)}\n")

ok = 0
dead = 0
other = 0

for i, url in enumerate(urls):
    try:
        r = requests.head(url, timeout=10, headers=headers, allow_redirects=True)
        if r.status_code == 200:
            ok += 1
        elif r.status_code == 404:
            dead += 1
            print(f"❌ 404: {url}")
        else:
            other += 1
            print(f"⚠️ {r.status_code}: {url}")
    except Exception as e:
        other += 1
        print(f"⚠️ ERR: {url} - {e}")
    
    if (i + 1) % 30 == 0:
        print(f"  ...checked {i+1}/{len(urls)}")
    
    time.sleep(0.3)

print(f"\n{'='*50}")
print(f"✅ 200 OK: {ok}")
print(f"❌ 404 Dead: {dead}")
print(f"⚠️ Other: {other}")
