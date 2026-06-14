import requests, hashlib, time, json, sys, urllib.request

# 1. Get token
resp = requests.get('http://127.0.0.1:18432/get_token', timeout=5)
token = resp.text.strip()
if not token.startswith('Bearer'):
    token = 'Bearer ' + token

# 2. Sign headers
appid = '100003'
secret = '38d2391985e2369a5fb8227d8e6cd5e5'
ts = str(int(time.time()))
sign = hashlib.md5((appid + '&' + ts + '&' + secret).encode()).hexdigest()

# 3. Generate images
descriptions = [
    "Chrome browser notification settings page, modern dark UI showing notification permission list with allow/block/remove buttons, clean tech illustration style",
    "Chrome browser settings page showing remove all site notification permissions button highlighted with red accent, clean minimalist design",
    "Windows 11 system settings notification page showing Google Chrome toggle switch being turned off, modern UI illustration",
    "Chrome browser notification management flowchart diagram showing three levels: website notifications, Chrome tips, system notifications with arrows, tech style",
    "A Chrome browser window with notification bell icon crossed out with a red line, dark blue background, modern flat design illustration for article cover"
]

output_dir = r'C:\Projects\chromebest\static\images\tips\chrome-notification-settings'
import os
os.makedirs(output_dir, exist_ok=True)

for i, desc in enumerate(descriptions):
    headers = {
        'Authorization': token,
        'X-Auth-Appid': appid,
        'X-Auth-TimeStamp': ts,
        'X-Auth-Sign': sign,
        'Content-Type': 'application/json'
    }
    body = json.dumps({"text": desc})
    try:
        resp = requests.post('https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image',
                           headers=headers, data=body, timeout=60)
        result = resp.json()
        if result.get('code') == 0 and result.get('data', {}).get('image_url'):
            img_url = result['data']['image_url']
            filename = f'img-{i+1}.jpg' if i < 4 else 'cover.jpg'
            filepath = os.path.join(output_dir, filename)
            urllib.request.urlretrieve(img_url, filepath)
            print(f'[{i+1}/5] OK: {filename} -> {img_url}')
        else:
            print(f'[{i+1}/5] FAIL: {result}')
    except Exception as e:
        print(f'[{i+1}/5] ERROR: {e}')
    time.sleep(1)

print('\nDone!')
