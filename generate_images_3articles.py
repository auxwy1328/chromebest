# -*- coding: utf-8 -*-
"""批量生成 chromebest.com 3篇新文章的配图 + 封面图，自动裁剪水印并插入Markdown"""
import requests, hashlib, time, os, re, json, sys
from PIL import Image
from io import BytesIO

# ============== 配置 ==============
SKILL_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-autoclaw", "skills", "autoglm-generate-image")
GEN_SCRIPT = os.path.join(SKILL_DIR, "generate-image.py")
BASE_DIR = r"C:\Projects\chromebest\static\images"

# 3篇文章的图片规划
# (section, slug, 图片类型, 图片描述)
IMAGE_PLAN = [
    # 第23篇: Chrome更新失败修复
    ("tips", "chrome-update-failed-fix", "cover", "Chrome浏览器关于页面截图风格，显示版本号和更新状态，深色主题界面，专业干净的设计"),
    ("tips", "chrome-update-failed-fix", "body1", "Windows服务管理器界面，显示Google Update服务正在运行，专业系统管理界面截图效果"),
    ("tips", "chrome-update-failed-fix", "body2", "Chrome设置页面网络代理配置界面，深色主题，显示代理服务器设置选项，真实UI风格"),
    ("tips", "chrome-update-failed-fix", "body3", "Chrome浏览器关于页面，更新下载进度条，显示正在检查更新状态，深色主题"),

    # 第24篇: Chrome同步设置
    ("tips", "chrome-sync-settings-guide", "cover", "Chrome浏览器登录同步界面，显示Google账号头像和同步选项开关，深色主题，现代UI设计"),
    ("tips", "chrome-sync-settings-guide", "body1", "Chrome同步设置页面，显示书签密码历史记录等同步项目列表，每个项目有开关按钮，深色主题"),
    ("tips", "chrome-sync-settings-guide", "body2", "手机和电脑多设备同步示意图，Chrome浏览器图标在笔记本和手机之间有数据流动效果，科技感插画"),
    ("tips", "chrome-sync-settings-guide", "body3", "Chrome多用户个人资料切换界面，显示多个头像图标，深色主题浏览器UI风格"),

    # 第25篇: Chrome默认浏览器设置
    ("tips", "chrome-set-default-browser-guide", "cover", "Chrome浏览器Logo标志放在深蓝色渐变背景上，简洁现代的设计，品牌感强"),
    ("tips", "chrome-set-default-browser-guide", "body1", "Windows 11设置页面默认应用界面，显示浏览器选项列表，Chrome被选中，现代Windows UI风格"),
    ("tips", "chrome-set-default-browser-guide", "body2", "电脑浏览器安全防护概念图，盾牌图标保护浏览器，深色背景科技感设计"),
    ("tips", "chrome-set-default-browser-guide", "body3", "Windows控制面板默认程序设置界面，显示Chrome被设为默认Web浏览器，专业系统界面截图效果"),
]

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
                print(f"  API error (attempt {attempt+1}): {data.get('msg', 'unknown')}")
                time.sleep(3)
        except Exception as e:
            print(f"  Network error (attempt {attempt+1}): {e}")
            time.sleep(3)
    return None

def download_and_crop(url, save_path):
    """下载图片并裁剪水印 (97%w x 88%h)"""
    r = requests.get(url, timeout=30)
    img = Image.open(BytesIO(r.content))
    w, h = img.size
    cropped = img.crop((0, 0, int(w * 0.97), int(h * 0.88)))
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cropped.save(save_path, "JPEG", quality=92)
    print(f"  Saved: {save_path} ({cropped.size[0]}x{cropped.size[1]})")

def insert_body_image(md_path, img_path, alt_text, after_h2_pattern=None):
    """在Markdown正文中插入图片（在指定H2标题后）"""
    text = open(md_path, 'r', encoding='utf-8').read()
    img_tag = f'\n![{alt_text}]({img_path})\n'
    
    if after_h2_pattern:
        idx = text.find(after_h2_pattern)
        if idx >= 0:
            # 在H2标题后的第一个段落末尾插入
            next_newline = text.find('\n', idx)
            insert_pos = next_newline + 1 if next_newline >= 0 else idx + len(after_h2_pattern)
            text = text[:insert_pos] + img_tag + text[insert_pos:]
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(text)
    print(f"  Inserted image into {os.path.basename(md_path)}")

def main():
    print(f"共 {len(IMAGE_PLAN)} 张图片待生成\n")
    
    # 统计
    success = 0
    failed = 0
    
    for i, (section, slug, img_type, prompt) in enumerate(IMAGE_PLAN):
        print(f"[{i+1}/{len(IMAGE_PLAN)}] {section}/{slug} - {img_type}")
        
        img_dir = os.path.join(BASE_DIR, section, slug)
        img_name = f"cover.jpg" if img_type == "cover" else f"{img_type}.jpg"
        save_path = os.path.join(img_dir, img_name)
        
        # 检查是否已存在
        if os.path.exists(save_path):
            print(f"  SKIP (already exists): {img_name}")
            success += 1
            continue
        
        # 生成图片
        url = generate_image(prompt)
        if not url:
            print(f"  FAILED to generate")
            failed += 1
            continue
        
        # 下载并裁剪
        try:
            download_and_crop(url, save_path)
            success += 1
        except Exception as e:
            print(f"  FAILED to download/crop: {e}")
            failed += 1
        
        time.sleep(2)
    
    print(f"\n完成: {success} 成功, {failed} 失败")
    
    # 插入正文配图到Markdown
    print("\n--- 插入正文配图到Markdown ---")
    
    md_base = r"C:\Projects\chromebest\content"
    
    insert_plan = [
        ("tips", "chrome-update-failed-fix.md", "body1", "Chrome更新服务设置", "## 错误 0：更新程序无法启动"),
        ("tips", "chrome-update-failed-fix.md", "body2", "Chrome网络代理设置", "## 错误 3：网络连接被中断"),
        ("tips", "chrome-update-failed-fix.md", "body3", "Chrome更新检查进度", "## 终极方案：手动更新"),
        
        ("tips", "chrome-sync-settings-guide.md", "body1", "Chrome同步设置选项", "## 手机端开启同步"),
        ("tips", "chrome-sync-settings-guide.md", "body2", "Chrome多设备同步示意", "## 选择性同步建议"),
        ("tips", "chrome-sync-settings-guide.md", "body3", "Chrome个人资料切换", "## 同步常见问题"),
        
        ("tips", "chrome-set-default-browser-guide.md", "body1", "Windows11默认应用设置", "## Win10 设置 Chrome 为默认浏览器"),
        ("tips", "chrome-set-default-browser-guide.md", "body2", "浏览器安全防护", "## 默认浏览器被恶意软件篡改怎么修复"),
        ("tips", "chrome-set-default-browser-guide.md", "body3", "Windows默认程序设置", "## 为什么默认浏览器这么容易被改"),
    ]
    
    for section, md_file, img_type, alt_text, after_h2 in insert_plan:
        slug = md_file.replace('.md', '')
        img_path = f"/images/{section}/{slug}/{img_type}.jpg"
        md_path = os.path.join(md_base, section, md_file)
        
        if os.path.exists(md_path):
            insert_body_image(md_path, img_path, alt_text, after_h2)
        else:
            print(f"  SKIP (file not found): {md_file}")

if __name__ == "__main__":
    main()
