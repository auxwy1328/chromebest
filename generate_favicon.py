# -*- coding: utf-8 -*-
"""生成 chromebest.com 的 favicon（Chrome 四色圆形风格）"""
from PIL import Image, ImageDraw, ImageFont
import os

STATIC = r"C:\Projects\chromebest\static"

def draw_chrome_circle(size, filename):
    """画一个 Chrome 风格的简化 logo：圆形，红黄绿蓝四色"""
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    cx, cy = size // 2, size // 2
    r = int(size * 0.45)
    
    # 简化版 Chrome logo：三色扇形 + 蓝色中心圆
    import math
    
    # 红色（右上扇形，0° 到 120°）
    draw.pieslice([cx-r, cy-r, cx+r, cy+r], -30, 90, fill='#EA4335')
    # 黄色（左下扇形，120° 到 240°）
    draw.pieslice([cx-r, cy-r, cx+r, cy+r], 90, 210, fill='#FBBC05')
    # 绿色（右下扇形，240° 到 360°）
    draw.pieslice([cx-r, cy-r, cx+r, cy+r], 210, 330, fill='#34A853')
    
    # 蓝色中心圆
    cr = int(r * 0.48)
    draw.ellipse([cx-cr, cy-cr, cx+cr, cy+cr], fill='#4285F4')
    
    # 中心白字 "C"（用简单方式）
    try:
        font = ImageFont.truetype("arial.ttf", int(size * 0.38))
    except:
        font = ImageFont.load_default()
    
    text = "C"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    draw.text((cx - tw/2, cy - th/2 - 2), text, fill='white', font=font)
    
    filepath = os.path.join(STATIC, filename)
    img.save(filepath, 'PNG')
    print(f"Saved: {filepath} ({size}x{size})")
    return img

# 生成三种尺寸
draw_chrome_circle(180, "apple-touch-icon.png")

# favicon.ico (32x32)
img32 = draw_chrome_circle(32, "favicon-32x32.png")

# 16x16
draw_chrome_circle(16, "favicon-16x16.png")

# 生成 favicon.ico（包含 16x16 和 32x32）
from PIL import Image as PILImage
img16 = PILImage.open(os.path.join(STATIC, "favicon-16x16.png"))
img180 = PILImage.open(os.path.join(STATIC, "apple-touch-icon.png"))

# ICO 格式
img32.save(os.path.join(STATIC, "favicon.ico"), format='ICO', sizes=[(16,16), (32,32)])
print("Saved favicon.ico")

print("\nDone! All favicons generated.")
