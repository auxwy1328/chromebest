"""Generate 5 images for chrome-default-browser article using AutoGLM API."""
import urllib.request, json, hashlib, time, os
from PIL import Image
from io import BytesIO

TOKEN_URL = "http://127.0.0.1:18432/get_token"
API_URL = "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image"
OUTPUT_DIR = r"C:\Projects\chromebest\static\images\tips\chrome-default-browser"

PROMPTS = {
    "cover.jpg": "A clean realistic mockup showing Chrome browser icon selected as default browser in Windows 11 settings, with Edge unselected, blue Windows 11 settings style, high quality UI screenshot style",
    "win11-settings.jpg": "A realistic mockup of Windows 11 Settings app showing Default Apps page with browser selection list, Google Chrome highlighted and selected as default, blue Windows 11 UI style, detailed settings interface",
    "mac-settings.jpg": "A realistic mockup of macOS Ventura System Settings showing default browser dropdown menu with Google Chrome selected, Apple style design, clean light interface, detailed system preferences",
    "android-default.jpg": "A realistic mockup of Android phone settings showing default apps browser selection screen, with Google Chrome checked as default browser, Samsung or Google Pixel style, dark theme phone UI",
    "edge-hijack.jpg": "A realistic Chrome browser settings page showing default browser prompt dialog, Chrome warning message about Edge taking over as default, professional web browser interface mockup",
}

def get_token():
    ts = str(int(time.time()))
    sig = hashlib.md5(f'100003&{ts}&38d2391985e2369a5fb8227d8e6cd5e5'.encode()).hexdigest()
    url = f'{TOKEN_URL}?aid=100003&timestamp={ts}&sign={sig}'
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req, timeout=10)
    body = resp.read().decode().strip()
    if not body.startswith("Bearer"):
        body = "Bearer " + body
    return body

def make_auth_headers():
    ts = str(int(time.time()))
    sig = hashlib.md5(f'100003&{ts}&38d2391985e2369a5fb8227d8e6cd5e5'.encode()).hexdigest()
    return {
        "X-Auth-Appid": "100003",
        "X-Auth-TimeStamp": ts,
        "X-Auth-Sign": sig,
    }

def generate_image(token, prompt):
    headers = make_auth_headers()
    headers["Authorization"] = token
    headers["Content-Type"] = "application/json"
    body = json.dumps({"text": prompt}).encode()
    req = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
    resp = urllib.request.urlopen(req, timeout=120)
    result = json.loads(resp.read().decode())
    return result

def download_and_crop(url, output_path):
    req = urllib.request.Request(url)
    resp = urllib.request.urlopen(req, timeout=60)
    img_data = resp.read()
    img = Image.open(BytesIO(img_data)).convert("RGB")
    w, h = img.size
    img = img.crop((0, 0, int(w * 0.97), int(h * 0.92)))
    img.save(output_path, "JPEG", quality=92)
    print(f"  Saved: {output_path} ({img.size})")

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    token = get_token()
    print(f"Token: {token[:50]}...")

    for filename, prompt in PROMPTS.items():
        output_path = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(output_path):
            print(f"SKIP (exists): {filename}")
            continue
        print(f"\nGenerating: {filename}")
        try:
            result = generate_image(token, prompt)
            print(f"  API result keys: {list(result.keys())}, code: {result.get('code')}")
            if result.get("code") != 0:
                print(f"  ERROR: {result.get('msg')}")
                continue
            image_url = result.get("data", {}).get("image_url")
            if not image_url:
                print(f"  No image_url in result: {json.dumps(result)[:500]}")
                continue
            print(f"  Image URL: {image_url[:100]}...")
            download_and_crop(image_url, output_path)
        except Exception as e:
            print(f"  ERROR: {e}")

if __name__ == "__main__":
    main()
