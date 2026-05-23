# -*- coding: utf-8 -*-
"""批量生成 chromebest.com 22篇文章的配图（封面+正文），自动裁剪水印并插入Markdown"""
import requests, hashlib, time, os, re, base64, json
from PIL import Image
from io import BytesIO

SKILL_DIR = os.path.join(os.path.expanduser("~"), ".openclaw-autoclaw", "skills", "autoglm-generate-image")
BASE_DIR = r"C:\Projects\chromebest\static\images"
CONTENT_DIR = r"C:\Projects\chromebest\content"

# 22篇文章的图片规划: (section, slug, cover_prompt, body_prompts[3])
IMAGE_PLAN = [
    # compare
    ("compare", "chrome-desktop-vs-mobile-comparison",
     "Chrome浏览器桌面版和手机版并排展示对比，深色科技感背景，现代UI设计",
     ["Chrome桌面版浏览器界面截图风格，显示多个标签页和书签栏，深色主题",
      "Chrome手机版浏览器界面截图风格，显示简洁的移动端UI，深色主题",
      "电脑和手机图标对比图，数据同步箭头在两个设备之间流动，科技插画风格"]),

    ("compare", "chrome-vs-edge-2026",
     "Chrome和Edge浏览器Logo对比，左右排列，深蓝科技感背景，简洁现代设计",
     ["Chrome浏览器设置页面截图风格，显示性能和功能选项，深色主题",
      "Edge浏览器设置页面截图风格，显示Copilot和性能选项，深色主题",
      "两个浏览器性能测试对比图表风格，内存占用和速度数据可视化，专业设计"]),

    ("compare", "chrome-vs-edge-vs-firefox-2026",
     "三个浏览器Logo三角排列，Chrome红黄绿蓝、Edge蓝绿、Firefox橙红，深色背景",
     ["三个浏览器功能对比表格截图风格，行项清晰可读，深色主题设计",
      "三个浏览器内存占用对比条形图，Chrome绿色、Edge蓝色、Firefox橙色，简洁数据可视化",
      "浏览器扩展商店页面截图风格，显示扩展数量对比，深色主题"]),

    # download
    ("download", "chrome-offline-installer-download",
     "Chrome浏览器安装包下载页面概念图，大号下载箭头和进度条，深色科技感背景",
     ["Chrome官方网站下载页面截图风格，显示下载按钮和版本号，深色主题",
      "Windows系统设置中程序安装界面截图风格，显示安装进度条，专业UI",
      "Chrome离线安装包和在线安装包对比示意图，文件大小差异可视化"]),

    # plugins
    ("plugins", "chrome-ad-blocker-comparison",
     "Chrome广告拦截插件概念图，盾牌挡住广告弹窗，深色背景科技感设计",
     ["uBlock Origin插件设置界面截图风格，显示过滤规则和统计，深色主题",
      "网页广告被拦截后的清洁效果对比，左侧广告满屏右侧干净整洁，专业对比设计",
      "Chrome扩展商店广告拦截插件列表截图风格，显示评分和用户数"]),

    ("plugins", "chrome-ad-blocker-extension-recommendation",
     "五个广告拦截插件图标排列展示，深色渐变背景，现代卡片式设计",
     ["Chrome扩展管理页面截图风格，显示已安装的拦截插件列表，深色主题",
      "uBlock Origin配置界面截图风格，显示自定义规则列表，专业UI",
      "广告拦截前后网页对比效果，广告区域变空白，示意性强"]),

    ("plugins", "chrome-essential-extensions",
     "Chrome扩展插件图标矩阵排列，10个彩色图标整齐排列，深色背景现代设计",
     ["Chrome扩展商店首页截图风格，显示推荐扩展卡片，深色主题",
      "Chrome扩展管理器界面截图风格，显示已启用扩展的开关列表",
      "工作效率工具类扩展概念图，日历、笔记、翻译等图标组合"]),

    ("plugins", "chrome-password-manager-comparison",
     "密码锁和盾牌组合图标，安全概念，深蓝色科技感背景，专业设计",
     ["Chrome内置密码管理器界面截图风格，显示已保存的密码列表，深色主题",
      "Bitwarden密码管理器界面截图风格，显示密码库和分类，深色主题",
      "密码安全强度对比条形图，四个密码管理器安全评分可视化"]),

    ("plugins", "chrome-screenshot-extensions",
     "浏览器截图工具概念图，剪刀裁剪网页图标，深色渐变背景现代设计",
     ["Chrome网页截图插件操作界面截图风格，显示截图区域选择框，深色主题",
      "Awesome Screenshot插件设置界面截图风格，显示编辑工具栏，专业UI",
      "截图编辑后的效果展示，标注箭头和文字注释，示意性强"]),

    ("plugins", "chrome-translation-extension-comparison",
     "翻译插件概念图，地球图标配多语言文字气泡，深色科技感背景",
     ["Chrome网页翻译效果截图风格，显示中英文对照翻译，深色主题",
      "Google翻译插件弹出窗口截图风格，显示翻译选项和语言选择，专业UI",
      "五个翻译插件功能对比表格，准确率和速度数据可视化"]),

    # tips
    ("tips", "chrome-appearance-customization",
     "Chrome浏览器个性化主题画廊概念图，多彩渐变色主题卡片排列，现代设计",
     ["Chrome外观设置页面截图风格，显示主题选择和颜色自定义选项，深色主题",
      "Chrome Web Store主题商店截图风格，显示多个主题预览卡片",
      "Chrome浏览器应用了自定义主题后的效果，多彩标签栏和背景"]),

    ("tips", "chrome-bookmarks-management",
     "书签管理概念图，文件夹和标签图标整齐排列，蓝色调科技感背景",
     ["Chrome书签管理器界面截图风格，显示书签文件夹树状结构，深色主题",
      "Chrome书签栏截图风格，显示多个书签文件夹和快捷方式",
      "书签导入导出设置界面截图风格，显示HTML文件导入选项"]),

    ("tips", "chrome-common-problems-in-china",
     "中国地图和Chrome图标组合，网络连接概念，红金色调背景设计",
     ["Chrome无法加载网页的错误页面截图风格，显示ERR_CONNECTION错误，深色主题",
      "Chrome代理设置界面截图风格，显示系统代理配置选项",
      "Chrome在国内使用问题排查流程图，步骤清晰的专业设计"]),

    ("tips", "chrome-crash-fix",
     "Chrome崩溃修复概念图，扳手工具和Chrome图标组合，红色警示风格背景",
     ["Chrome任务管理器界面截图风格，显示进程列表和内存占用，深色主题",
      "Chrome扩展管理页面截图风格，显示禁用扩展的开关，深色主题",
      "Chrome无头模式启动命令行界面，显示启动参数，终端风格"]),

    ("tips", "chrome-devtools-beginner-guide",
     "Chrome开发者工具界面截图风格，显示元素检查和控制台面板，暗色代码主题",
     ["Chrome DevTools Elements面板截图风格，显示HTML结构和CSS样式，暗色代码主题",
      "Chrome DevTools Network面板截图风格，显示网络请求瀑布流和加载时间",
      "Chrome DevTools Console面板截图风格，显示JavaScript调试输出，暗色主题"]),

    ("tips", "chrome-incognito-mode-guide",
     "Chrome无痕模式概念图，戴墨镜的Chrome图标，深色私密风格背景设计",
     ["Chrome无痕模式窗口截图风格，显示无痕图标和简洁工具栏，深色主题",
      "无痕模式与普通模式对比图，左侧正常窗口右侧无痕窗口，专业对比设计",
      "Chrome隐私设置中无痕模式相关选项截图风格，深色主题"]),

    ("tips", "chrome-keyboard-shortcuts",
     "键盘按键组合概念图，Ctrl+Shift+N等快捷键悬浮展示，深色科技感背景",
     ["Chrome快捷键操作演示截图风格，显示Ctrl+T打开新标签的效果",
      "Chrome标签页管理快捷键演示，多个标签页排列有序，专业UI展示",
      "快捷键速查表格设计，按场景分类排列，清晰易读"]),

    ("tips", "chrome-memory-optimization",
     "Chrome内存优化概念图，芯片和内存条图标组合，绿色性能风格背景",
     ["Chrome任务管理器截图风格，显示各标签页和扩展的内存占用数据，深色主题",
      "Chrome性能设置页面截图风格，显示硬件加速和内存节省选项",
      "内存优化前后对比数据可视化，内存占用降低的图表展示"]),

    ("tips", "chrome-mobile-tips",
     "手机端Chrome浏览器概念图，Chrome图标在手机屏幕上，深色移动端风格",
     ["Android版Chrome浏览器界面截图风格，显示底部标签栏和菜单，深色主题",
      "iPhone版Chrome浏览器界面截图风格，显示iOS风格底部工具栏",
      "Chrome手机版设置页面截图风格，显示数据节省和同步选项"]),

    ("tips", "chrome-privacy-settings-guide",
     "Chrome隐私安全概念图，锁盾牌和指纹图标组合，深蓝安全风格背景",
     ["Chrome隐私设置页面截图风格，显示第三方Cookie和安全浏览选项，深色主题",
      "Chrome安全检查工具截图风格，显示密码泄露检测和建议",
      "Chrome清除浏览数据对话框截图风格，显示时间范围和数据类型选项"]),

    ("tips", "chrome-secure-dns-setup",
     "DNS安全概念图，盾牌和服务器节点网络连接，蓝绿色科技感背景",
     ["Chrome安全DNS设置页面截图风格，显示DNS-over-HTTPS选项，深色主题",
      "DNS解析流程示意图，浏览器到DNS服务器的加密连接，科技插画风格",
      "Chrome隐私和安全设置中DNS相关选项截图风格，深色主题"]),

    ("tips", "chrome-video-download-guide",
     "视频下载概念图，播放按钮和下载箭头组合，红蓝渐变科技感背景",
     ["Chrome浏览器中视频播放页面截图风格，显示视频播放器和控制栏，深色主题",
      "Chrome扩展商店视频下载插件截图风格，显示插件列表和评分",
      "视频下载工具界面截图风格，显示下载进度和格式选择选项"]),
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
    r = requests.get(url, timeout=30)
    img = Image.open(BytesIO(r.content))
    w, h = img.size
    cropped = img.crop((0, 0, int(w * 0.97), int(h * 0.88)))
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    cropped.save(save_path, "JPEG", quality=92)

def get_h2_headings(md_path):
    """Get all H2 headings from a markdown file"""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    return re.findall(r'^## (.+)$', text, re.MULTILINE)

def insert_images_into_md(md_path, slug, section, body_paths):
    """Insert body images after every other H2 heading"""
    with open(md_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    headings = re.finditer(r'^(## .+)$', text, re.MULTILINE)
    heading_positions = [(m.start(), m.group(1)) for m in headings]
    
    # Insert image after 2nd, 4th, 6th H2 (spread evenly)
    insert_after = [1, 3, 5]  # 0-indexed positions in headings list
    
    inserted = 0
    for idx in reversed(insert_after):
        if idx < len(heading_positions) and inserted < len(body_paths):
            pos, heading = heading_positions[idx]
            # Find end of heading line
            end_of_line = text.find('\n', pos)
            if end_of_line < 0:
                end_of_line = pos + len(heading)
            img_path = body_paths[inserted]
            alt = heading.replace('# ', '').strip()[:20]
            img_tag = f'\n![{alt}]({img_path})\n'
            text = text[:end_of_line+1] + img_tag + text[end_of_line+1:]
            inserted += 1
    
    # If not enough H2s, append remaining images before FAQ section
    if inserted < len(body_paths):
        faq_match = re.search(r'^## 常见问题', text, re.MULTILINE)
        if faq_match:
            for i in range(inserted, len(body_paths)):
                img_tag = f'\n![配图]({body_paths[i]})\n'
                text = text[:faq_match.start()] + img_tag + text[faq_match.start():]
    
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(text)

def main():
    total_images = len(IMAGE_PLAN) * 4  # 22 * 4 = 88
    print(f"共 {len(IMAGE_PLAN)} 篇文章，{total_images} 张图片待生成\n", flush=True)
    
    success = 0
    failed = 0
    img_plan_list = []  # track (section, slug, img_type, save_path) for MD insertion
    
    for i, (section, slug, cover_prompt, body_prompts) in enumerate(IMAGE_PLAN):
        print(f"\n[{i+1}/{len(IMAGE_PLAN)}] {section}/{slug}")
        
        img_dir = os.path.join(BASE_DIR, section, slug)
        
        # Cover image
        cover_path = os.path.join(img_dir, "cover.jpg")
        if os.path.exists(cover_path):
            print(f"  cover: SKIP (exists)")
            success += 1
        else:
            print(f"  cover: generating...")
            url = generate_image(cover_prompt)
            if url:
                try:
                    download_and_crop(url, cover_path)
                    print(f"  cover: OK")
                    success += 1
                except Exception as e:
                    print(f"  cover: FAIL ({e})")
                    failed += 1
            else:
                print(f"  cover: FAIL (no url)")
                failed += 1
            time.sleep(2)
        
        # Body images
        body_paths = []
        for j, prompt in enumerate(body_prompts):
            img_name = f"body{j+1}.jpg"
            save_path = os.path.join(img_dir, img_name)
            img_web_path = f"/images/{section}/{slug}/{img_name}"
            
            if os.path.exists(save_path):
                print(f"  {img_name}: SKIP (exists)")
                success += 1
            else:
                print(f"  {img_name}: generating...")
                url = generate_image(prompt)
                if url:
                    try:
                        download_and_crop(url, save_path)
                        print(f"  {img_name}: OK")
                        success += 1
                    except Exception as e:
                        print(f"  {img_name}: FAIL ({e})")
                        failed += 1
                else:
                    print(f"  {img_name}: FAIL (no url)")
                    failed += 1
                time.sleep(2)
            
            body_paths.append(img_web_path)
        
        # Insert images into markdown
        md_path = os.path.join(CONTENT_DIR, section, f"{slug}.md")
        if os.path.exists(md_path):
            insert_images_into_md(md_path, slug, section, body_paths)
            print(f"  md: images inserted")
    
    print(f"\n{'='*50}")
    print(f"完成: {success} 成功, {failed} 失败, 共 {total_images} 张")

if __name__ == "__main__":
    main()
