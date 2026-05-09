# -*- coding: utf-8 -*-
"""Generate 25 OG images for chromebest.com articles (1200x630)"""
import requests, hashlib, time, os, re, base64
from PIL import Image
from io import BytesIO

SKILL_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-autoclaw", "skills", "autoglm-generate-image")
BASE_DIR = r"C:\Projects\chromebest\static\images"
CONTENT_DIR = r"C:\Projects\chromebest\content"
OG_SIZE = (1200, 630)

def get_token():
    r = requests.get("http://127.0.0.1:18432/get_token", timeout=5)
    token = r.text.strip()
    if not token.startswith("Bearer"):
        token = "Bearer " + token
    return token

def generate_image(prompt):
    token = get_token()
    ts = str(int(time.time()))
    sign = hashlib.md5(("100003&" + ts + "&38d2391985e2369a5fb8227d8e6cd5e5").encode()).hexdigest()
    headers = {
        "Authorization": token,
        "Content-Type": "application/json",
        "X-Auth-Appid": "100003",
        "X-Auth-TimeStamp": ts,
        "X-Auth-Sign": sign
    }
    for attempt in range(3):
        try:
            r = requests.post(
                "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image",
                headers=headers,
                json={"text": prompt},
                timeout=60
            )
            data = r.json()
            if data.get("code") == 0:
                return data["data"]["image_url"]
            else:
                print(f"  API error ({attempt+1}): {data.get('msg', 'unknown')}")
                time.sleep(3)
        except Exception as e:
            print(f"  Network error ({attempt+1}): {e}")
            time.sleep(3)
    return None

def download_crop_resize(url, save_path):
    """Download, crop watermark (97%x88%), resize to 1200x630"""
    r = requests.get(url, timeout=30)
    img = Image.open(BytesIO(r.content))
    w, h = img.size
    # Crop watermark
    cropped = img.crop((0, 0, int(w * 0.97), int(h * 0.88)))
    # Resize to OG size
    resized = cropped.resize(OG_SIZE, Image.LANCZOS)
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    resized.save(save_path, "JPEG", quality=92)

def get_all_articles():
    """Get all articles with section, slug, title"""
    articles = []
    for root, dirs, files in os.walk(CONTENT_DIR):
        for fname in files:
            if not fname.endswith('.md'):
                continue
            slug = fname.replace('.md', '')
            section = os.path.basename(root)
            fpath = os.path.join(root, fname)
            with open(fpath, 'r', encoding='utf-8') as f:
                text = f.read()
            title_match = re.search(r'^title:\s*"(.+?)"', text, re.MULTILINE)
            title = title_match.group(1) if title_match else slug
            articles.append((section, slug, title))
    return sorted(articles, key=lambda x: (x[0], x[1]))

def main():
    articles = get_all_articles()
    print(f"Total articles: {len(articles)}\n")
    
    success = 0
    failed = 0
    
    # OG image prompts - unique for each article based on topic
    og_prompts = {
        "chrome-desktop-vs-mobile-comparison": "Chrome desktop and mobile browsers side by side comparison, professional tech banner design 1200x630",
        "chrome-vs-edge-2026": "Chrome vs Edge browser comparison with performance metrics, modern tech banner style",
        "chrome-vs-edge-vs-firefox-2026": "Three browsers Chrome Edge Firefox comparison chart, professional data visualization banner",
        "chrome-offline-installer-download": "Chrome browser download installation concept with progress bar, clean tech banner design",
        "chrome-ad-blocker-comparison": "Chrome ad blocking shield concept, professional cybersecurity banner design",
        "chrome-ad-blocker-extension-recommendation": "Five ad blocker extension icons array, clean tech banner with gradient background",
        "chrome-essential-extensions": "Chrome extension grid showcase, productivity tools concept, modern tech banner",
        "chrome-password-manager-comparison": "Password security lock and shield concept, cybersecurity tech banner design",
        "chrome-screenshot-extensions": "Browser screenshot tool concept with crop scissors, clean tech banner",
        "chrome-translation-extension-comparison": "Translation language globe with speech bubbles, multilingual tech banner",
        "chrome-appearance-customization": "Chrome browser theme customization gallery, colorful gradient banner design",
        "chrome-bookmarks-management": "Bookmark folder organization concept, clean productivity tech banner",
        "chrome-common-problems-in-china": "Chrome browser usage in China with network connectivity concept, tech banner",
        "chrome-crash-fix": "Chrome crash fix concept with wrench tool and browser icon, red alert style banner",
        "chrome-devtools-beginner-guide": "Chrome DevTools code inspector panel, dark theme code editor banner",
        "chrome-incognito-mode-guide": "Chrome incognito mode privacy concept, dark stealth style tech banner",
        "chrome-keyboard-shortcuts": "Keyboard shortcut keys floating display, productivity tech banner design",
        "chrome-memory-optimization": "Chrome memory optimization with chip and RAM icons, green performance banner",
        "chrome-mobile-tips": "Chrome mobile browser on phone screen, mobile tech banner design",
        "chrome-privacy-settings-guide": "Chrome privacy shield and fingerprint protection concept, blue security banner",
        "chrome-secure-dns-setup": "DNS security encrypted connection network diagram, blue-green tech banner",
        "chrome-set-default-browser-guide": "Chrome logo as default browser on dark background, clean brand banner",
        "chrome-sync-settings-guide": "Multi-device sync concept with Chrome across laptop and phone, tech banner",
        "chrome-update-failed-fix": "Chrome update error fix concept with settings page, repair tech banner",
        "chrome-video-download-guide": "Video download concept with play button and download arrow, media tech banner",
    }
    
    for i, (section, slug, title) in enumerate(articles):
        print(f"[{i+1}/{len(articles)}] {section}/{slug}")
        
        og_path = os.path.join(BASE_DIR, section, slug, "og.jpg")
        
        if os.path.exists(og_path):
            print(f"  SKIP (exists)")
            success += 1
            continue
        
        fallback = "Chrome browser " + slug.replace("-", " ") + " topic banner"
        prompt = og_prompts.get(slug, fallback)
        
        url = generate_image(prompt)
        if not url:
            print(f"  FAILED")
            failed += 1
            continue
        
        try:
            download_crop_resize(url, og_path)
            print(f"  OK ({OG_SIZE[0]}x{OG_SIZE[1]})")
            success += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            failed += 1
        
        time.sleep(2)
    
    print(f"\n{'='*50}")
    print(f"Done: {success} success, {failed} failed")

if __name__ == "__main__":
    main()
