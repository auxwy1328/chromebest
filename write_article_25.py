# -*- coding: utf-8 -*-
import os, re

base = r'C:\Projects\chromebest\content\tips'
filepath = os.path.join(base, 'chrome-set-default-browser-guide.md')

article = """---
title: "Chrome 设为默认浏览器完整指南 + 被篡改后的修复方法"
date: 2026-05-06T08:00:00+08:00
slug: "chrome-set-default-browser-guide"
categories: ["使用技巧"]
tags: ["Chrome默认浏览器", "Chrome设为默认", "默认浏览器被篡改", "Win11默认浏览器", "浏览器劫持"]
description: "Chrome 设为默认浏览器的完整教程，覆盖 Win10、Win11 不同版本的操作步骤，以及默认浏览器被恶意软件篡改后的修复方法。"
pinned: false
tag_icon: "🌐"
tag_label: "设置指南"
tag_color: "green"
readtime: 10
screenshots: 8
excerpt: "Chrome 总是被改成其他浏览器？这篇教你正确设置默认浏览器，以及被篡改后怎么修回来。"
card_icon: "🌐"
card_label: "默认浏览器"
card_gradient: "#1a2a1a,#0d1117"
images: ["/images/chrome-set-default-browser-guide/cover.jpg"]
keywords: "Chrome默认浏览器,Chrome设为默认,默认浏览器被篡改,Win11默认浏览器,浏览器劫持修复"
---

安装了 Chrome 但每次点链接还是打开 Edge 或其他浏览器？或者默认浏览器被莫名其妙改成了别的？这两个问题困扰了不少人。

这篇文章分两部分：先讲怎么正确设置 Chrome 为默认浏览器（Win10 和 Win11 的操作不一样），再讲默认浏览器被篡改后怎么修复。

## Win11 设置 Chrome 为默认浏览器

Windows 11 的默认浏览器设置改动比较大，微软有意让 Edge 更难被替代。不过设置方法并不复杂。

### 方法一：通过 Chrome 自带设置（最简单）

1. 打开 Chrome
2. 点击右上角三个点 → 设置
3. 左侧菜单点击"默认浏览器"
4. 点击"设为默认浏览器"按钮
5. Windows 会弹出默认应用设置窗口，点击"切换 anyway"
6. 完成

这个方法在 Win11 22H2 及以上版本有效。Chrome 会自动帮你把 .htm、.html、http、https 等文件关联全部切换过来。

### 方法二：通过 Windows 设置

1. 打开 Windows 设置（Win + I）
2. 点击"应用" → "默认应用"
3. 搜索框输入 "Chrome"
4. 点击 Google Chrome
5. 在文件类型列表中，把 .htm、.html、http、https、.pdf 等全部改为 Chrome
6. 需要逐个点击并选择 Chrome，比较繁琐

**注意：** Win11 会弹出"推荐使用 Microsoft Edge"的提示，直接忽略就好。

## Win10 设置 Chrome 为默认浏览器

Win10 的设置比 Win11 简单得多，没有微软的"推荐"干扰。

### 方法一：通过 Chrome 自带设置

1. 打开 Chrome
2. 点击右上角三个点 → 设置
3. 点击"默认浏览器"部分
4. 点击"设为默认浏览器"
5. Windows 10 的控制面板会自动打开默认应用设置
6. 在"Web 浏览器"下拉菜单中选择 Google Chrome
7. 完成

### 方法二：通过控制面板

1. 打开控制面板（Win + R 输入 control）
2. 点击"程序" → "默认程序" → "设置默认程序"
3. 在左侧列表找到 Google Chrome
4. 点击"将此程序设为默认值"
5. 完成

Win10 这一步会自动把所有浏览器相关的文件关联都切换到 Chrome，比 Win11 省事很多。

## 手机端设置 Chrome 为默认浏览器

**Android：**

1. 打开手机"设置"
2. 找到"应用"或"应用管理"
3. 点击"默认应用"
4. 找到"浏览器"选项
5. 选择 Chrome

不同 Android 手机品牌（小米、华为、OPPO、vivo）的设置路径略有不同，但都在"设置 → 应用 → 默认应用"里。

**iPhone / iPad：**

iOS 从 14 版本开始支持更换默认浏览器。步骤：

1. 打开"设置"
2. 向下滚动找到 Chrome
3. 点击"默认浏览器应用"
4. 选择 Chrome

注意：iOS 上只能选 Safari 或已安装的第三方浏览器（Chrome、Firefox、Edge 等），但邮件中的链接仍然会用 Safari 打开，这是 iOS 的限制，无法修改。

## 默认浏览器总是被改成 Edge

这是 Windows 10/11 的一个"特性"——每次 Windows 系统更新（特别是大版本更新）都可能把默认浏览器重置回 Edge。微软的理由是"确保系统安全"，实际上就是推广 Edge。

**解决办法：**

1. 在 Windows 更新后，重新按上面的步骤设置 Chrome 为默认浏览器
2. 如果你用的是 Win11，Chrome 设置里有"让 Chrome 保持为默认浏览器"的选项，建议开启
3. 安装完 Windows 更新后不要急着重启，先检查默认浏览器有没有被改

## 默认浏览器被恶意软件篡改怎么修复

比 Windows 改默认浏览器更恶心的是恶意软件篡改。典型表现：

- 默认浏览器被改成一个你不认识的浏览器（如"安全浏览器"、"极速浏览器"等）
- 每次开机弹出一个浏览器广告页
- 浏览器主页被改成某个导航站，改不回来
- 任务栏多了一个浏览器图标，卸载了又自动装回来

如果你遇到以上任何一种情况，按以下步骤排查修复：

### 第一步：卸载可疑软件

1. 打开"设置" → "应用" → "已安装的应用"
2. 按安装日期排序，找出你不记得安装的软件
3. 卸载所有可疑的浏览器、工具栏、优化助手类软件
4. 特别注意名称里带"安全""加速""清理""助手"的软件

### 第二步：修复默认浏览器设置

卸载可疑软件后，默认浏览器可能还是不对。按上面的 Win10/Win11 设置方法重新设置一次。

### 第三步：检查浏览器劫持

打开 Chrome，查看主页是否被篡改：

1. Chrome 设置 → 启动时 → 选择"打开特定网页或一组网页"
2. 检查列表里有没有你不认识的网址，有就删掉
3. 设置 → 搜索引擎 → 管理搜索引擎和网站搜索 → 检查默认搜索引擎是不是被改了

### 第四步：清理注册表残留（高级）

如果以上步骤都做了但问题还在，可能是注册表里还有残留：

1. 按 Win + R 输入 regedit 打开注册表编辑器
2. 导航到 HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\Shell\\Associations\\UrlAssociations\\http\\UserChoice
3. 检查 ProgId 的值是否为 ChromeHTML，如果不是，手动改过来
4. 同样检查 https 对应的注册表项
5. 重启电脑

⚠️ 修改注册表有风险，操作前建议先导出备份。如果不确定自己能操作正确，跳过这步。

### 第五步：用专业工具清理

如果手动清理搞不定，可以用以下工具：

- **AdwCleaner**（Malwarebytes 出品）：专门清理广告软件和浏览器劫持，免费且有效
- **HitmanPro**：可以扫描并清除深层恶意软件
- **火绒安全**：国内用户推荐，有浏览器保护功能，可以锁定默认浏览器防止被篡改

使用方法很简单：下载 → 全盘扫描 → 清理 → 重启电脑。

## 为什么默认浏览器这么容易被改

默认浏览器之争本质上是流量之争。浏览器市场占有率意味着搜索收入、扩展生态、用户数据——这些都是真金白银。

微软用系统更新强制推广 Edge，流氓软件用捆绑安装抢默认浏览器，各有各的目的。作为用户，我们能做的就是：

1. 安装软件时仔细看每一步，取消勾选"设为默认浏览器"
2. 定期检查默认浏览器设置有没有被改
3. 安装可靠的安全软件防护浏览器劫持

## 常见问题

### 设置 Chrome 为默认浏览器后点链接还是打开 Edge？

Windows 11 的某些内置组件（如小组件、搜索栏、Cortana）会强制使用 Edge 打开链接，这是微软的限制，无法修改。但正常点击桌面快捷方式、文件管理器里的链接、第三方应用里的链接，都会用 Chrome 打开。

### 为什么 Win11 不让我改默认浏览器？

Win11 没有禁止改默认浏览器，只是操作步骤比 Win10 多了。按本文的方法操作一定能改成功。如果点击"设为默认浏览器"没有反应，试试重启电脑后再操作。

### 安装软件时如何防止默认浏览器被改？

安装任何软件时，注意安装向导的每一步，尤其是"附加选项""推荐安装"这类页面。取消勾选所有"设为 XXX 为默认浏览器"的选项。建议使用自定义安装而非"一键安装"。

### 默认浏览器设置每次重启都变回去？

这说明有恶意软件在后台持续篡改。用 AdwCleaner 或火绒全盘扫描清理。如果清理后问题仍然存在，建议检查计划任务（Win + R 输入 taskschd.msc），禁用可疑的计划任务。

### Chrome 和 Edge 哪个更适合做默认浏览器？

从纯功能角度来说，两者几乎一样（都用 Chromium 内核）。Edge 在 Windows 上启动速度略快、内存占用略低（因为和系统深度集成）。Chrome 的优势在于扩展生态更丰富、跨平台同步更成熟。选哪个取决于你的使用习惯，没有绝对的好坏。
"""

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(article)

body = article.split('---')[2]
chinese_chars = len(re.findall(r'[\u4e00-\u9fff]', body))
faq_count = len(re.findall(r'### ', body))
print(f'Article 25 saved to {filepath}')
print(f'Chinese chars: {chinese_chars}')
print(f'FAQ count: {faq_count}')
