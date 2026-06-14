import hashlib, time, json, urllib.request, os, sys
from PIL import Image
from io import BytesIO

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo0MTMyNTcsImRldmljZV9pZCI6IjMzYmMzNTRjZjE5ZDk3ZTEwOTExNTVkNGNmNmQ0NGVjY2VkOTkwMmRlZjkyYWE2NWZkMjg2M2U0YjI5Y2VjNzkiLCJzb3VyY2VfaWQiOiJhdXRvY2xhd2FjY2Vzc190b2tlbiIsImd1aWQiOiIiLCJpc19ndWVzdCI6ZmFsc2UsInBvd2VyIjowLCJleHAiOjE3ODA1NjA0MDksImlhdCI6MTc4MDQ3NDAwOSwianRpIjoiMTMxNzg4NjU1MzYifQ.YG-AuWHt8Ai89jpyVC1CbEF1AHpqigl4onwvjAj7FFk"
APPID = "100003"
SECRET = "38d2391985e2369a5fb8227d8e6cd5e5"
OUTPUT_DIR = r"C:\Projects\chromebest\static\images\tips\chrome-pdf-edit"

descriptions = [
    ("cover.jpg", "Chrome browser PDF viewer interface, professional screenshot style, dark UI toolbar at top, PDF document open with text content, annotation tools visible, clean modern web browser look, high quality UI mockup"),
    ("annotate.jpg", "Chrome PDF annotation tools highlighted, a user highlighting text in yellow on a PDF document, annotation toolbar with highlighter pen and text tools, professional screenshot mockup, clean browser interface"),
    ("print-pdf.jpg", "Chrome browser print dialog showing Save as PDF option selected, destination dropdown showing Save as PDF, layout and color settings visible, professional UI screenshot mockup"),
    ("form-fill.jpg", "Interactive PDF form being filled in Chrome browser, text fields with typed content, checkboxes checked, professional document form interface, clean web browser mockup"),
    ("signature.jpg", "Digital signature being drawn on a PDF document in Chrome browser, signature pad area with handwritten signature, professional document signing interface mockup"),
]

def generate_image(desc):
    ts = str(int(time.time()))
    sign_str = f"{APPID}&{ts}&{SECRET}"
    sign = hashlib.md5(sign_str.encode()).hexdigest()
    
    url = "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image"
    headers = {
        "Authorization": TOKEN,
        "X-Auth-Appid": APPID,
        "X-Auth-TimeStamp": ts,
        "X-Auth-Sign": sign,
        "Content-Type": "application/json"
    }
    body = json.dumps({"text": desc}).encode()
    
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    for attempt in range(3):
        try:
            resp = urllib.request.urlopen(req, timeout=60)
            result = json.loads(resp.read().decode())
            if "data" in result and "image_url" in result["data"]:
                img_url = result["data"]["image_url"]
                img_resp = urllib.request.urlopen(img_url, timeout=30)
                img_data = img_resp.read()
                img = Image.open(BytesIO(img_data)).convert("RGB")
                w, h = img.size
                img = img.crop((0, 0, int(w * 0.97), int(h * 0.92)))
                return img
            elif "image" in result:
                import base64
                img_data = base64.b64decode(result["image"])
                img = Image.open(BytesIO(img_data)).convert("RGB")
                w, h = img.size
                img = img.crop((0, 0, int(w * 0.97), int(h * 0.92)))
                return img
            else:
                print(f"  Unexpected response: {json.dumps(result, ensure_ascii=False)[:200]}")
                return None
        except Exception as e:
            print(f"  Attempt {attempt+1} failed: {e}")
            time.sleep(2)
    return None

for filename, desc in descriptions:
    filepath = os.path.join(OUTPUT_DIR, filename)
    if os.path.exists(filepath) and os.path.getsize(filepath) > 10000:
        print(f"SKIP {filename} (already exists, {os.path.getsize(filepath)} bytes)")
        continue
    print(f"Generating {filename}...")
    img = generate_image(desc)
    if img:
        img.save(filepath, "JPEG", quality=92)
        print(f"  Saved {filename} ({os.path.getsize(filepath)} bytes)")
    else:
        print(f"  FAILED {filename}")

# Create og.jpg as copy of cover.jpg if not exists
og_path = os.path.join(OUTPUT_DIR, "og.jpg")
cover_path = os.path.join(OUTPUT_DIR, "cover.jpg")
if not os.path.exists(og_path) and os.path.exists(cover_path):
    img = Image.open(cover_path)
    img.save(og_path, "JPEG", quality=92)
    print(f"Created og.jpg from cover.jpg")

print("Done!")
