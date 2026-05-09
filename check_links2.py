# -*- coding: utf-8 -*-
"""Check sitemap for dead links - save results to file"""
import requests, time, re

SITEMAP_URL = "https://chromebest.com/sitemap.xml"
headers = {"User-Agent": "Mozilla/5.0 (compatible; SiteChecker/1.0)"}

r = requests.get(SITEMAP_URL, timeout=15, headers=headers)
urls = re.findall(r'<loc>([^<]+)</loc>', r.text)

results = {"ok": [], "dead": [], "other": []}

for i, url in enumerate(urls):
    try:
        r = requests.head(url, timeout=10, headers=headers, allow_redirects=True)
        if r.status_code == 200:
            results["ok"].append(url)
        elif r.status_code == 404:
            results["dead"].append(url)
        else:
            results["other"].append(f"{r.status_code}: {url}")
    except Exception as e:
        results["other"].append(f"ERR: {url} - {e}")
    time.sleep(0.3)

with open(r"C:\Projects\chromebest\link_check_results.txt", 'w', encoding='utf-8') as f:
    f.write(f"OK (200): {len(results['ok'])}\n")
    f.write(f"Dead (404): {len(results['dead'])}\n")
    for u in results['dead']:
        f.write(f"  {u}\n")
    f.write(f"Other: {len(results['other'])}\n")
    for u in results['other']:
        f.write(f"  {u}\n")
