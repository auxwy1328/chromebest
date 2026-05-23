# -*- coding: utf-8 -*-
"""Test single image generation"""
import requests, hashlib, time

def get_token():
    r = requests.get("http://127.0.0.1:18432/get_token", timeout=5)
    token = r.text.strip()
    if not token.startswith("Bearer"):
        token = "Bearer " + token
    return token

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

print("Generating test image...")
r = requests.post(
    "https://autoglm-api.zhipuai.cn/agentdr/v1/assistant/skills/generate-image",
    headers=headers,
    json={"text": "Chrome browser logo on dark background"},
    timeout=60
)
print(f"Status: {r.status_code}")
print(r.text[:500])
