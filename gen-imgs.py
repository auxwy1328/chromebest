import hashlib, json, urllib.request, time, os, sys
from PIL import Image
from io import BytesIO

articles = [
    ("tips/chrome-clear-cache", "Browser settings panel showing clear cache dialog, checkmarks on cached images option, clean modern UI illustration, blue and white color scheme"),
    ("tips/chrome-extensions-not-working", "Chrome extensions puzzle piece icons with wrench repair symbol, browser toolbar with extension icons, clean tech illustration, blue accent"),
]

try:
    req = urllib.request.Request('http://127.0.0.1:18432/get_token')
    with urllib.request.urlopen(req, timeout=10) as resp:
        token = resp.read().decode().strip()
    if not token.startswith('Bearer '): token = 'Bearer ' + token
except Exception as e:
    print('ERROR: ' + str(e)); sys.exit(1)

api_url = 'https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image'
crop_w, crop_h = 0.97, 0.88

for slug, desc in articles:
    out_dir = 'static/images/' + slug
    os.makedirs(out_dir, exist_ok=True)
    for img_type, prompt_suffix in [('cover', desc), ('body1', desc.replace('illustration', 'screenshot mockup').replace('clean modern UI', 'realistic app interface'))]:
        out_path = out_dir + '/' + img_type + '.jpg'
        if os.path.exists(out_path):
            print('SKIP: ' + out_path); continue
        print('Generating: ' + slug + '/' + img_type + '...')
        appid, ts = '100003', str(int(time.time()))
        sign = hashlib.md5((appid + '&' + ts + '&38d2391985e2369a5fb8227d8e6cd5e5').encode()).hexdigest()
        headers = {'Authorization': token, 'X-Auth-Appid': appid, 'X-Auth-TimeStamp': ts, 'X-Auth-Sign': sign, 'Content-Type': 'application/json'}
        data = json.dumps({'text': prompt_suffix}).encode()
        req = urllib.request.Request(api_url, data=data, headers=headers, method='POST')
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read())
            if result.get('code') == 0 and result.get('data', {}).get('image_url'):
                img_url = result['data']['image_url']
                with urllib.request.urlopen(img_url, timeout=30) as resp2:
                    img_data = resp2.read()
                img = Image.open(BytesIO(img_data))
                w, h = img.size
                img = img.crop((0, 0, int(w * crop_w), int(h * crop_h)))
                img.save(out_path, 'JPEG', quality=92)
                print('  Saved: ' + out_path + ' (' + str(os.path.getsize(out_path)//1024) + 'KB)')
        except Exception as e:
            print('  ERROR: ' + str(e))
        time.sleep(2)

print('Done!')
