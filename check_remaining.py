# -*- coding: utf-8 -*-
"""Check remaining article URLs for 404"""
import requests

urls = [
    "https://chromebest.com/compare/chrome-vs-edge-vs-firefox-2026/",
    "https://chromebest.com/compare/chrome-desktop-vs-mobile-comparison/",
    "https://chromebest.com/download/chrome-offline-installer-download/",
    "https://chromebest.com/plugins/chrome-ad-blocker-extension-recommendation/",
    "https://chromebest.com/plugins/chrome-appearance-customization/",
    "https://chromebest.com/plugins/chrome-bookmarks-management/",
]

for url in urls:
    try:
        r = requests.head(url, timeout=10, allow_redirects=True)
        print(f"{r.status_code} {url}")
    except Exception as e:
        print(f"ERR {url}: {e}")
