---
title: "Chrome 离线安装包下载教程：官方完整版地址 + 安装步骤详解"
date: 2026-05-05T21:00:00+08:00
slug: "chrome-offline-installer-download"
categories: ["下载安装"]
tags: ["Chrome下载", "Chrome离线安装", "Chrome完整版", "Chrome安装包", "Chrome安装教程"]
description: "Chrome 离线安装包官方下载地址大全，含 Windows 64 位和 32 位完整版。详细介绍在线安装包和离线安装包的区别，以及完整安装步骤。"
pinned: true
tag_icon: "📥"
tag_label: "下载安装"
tag_color: "orange"
readtime: 8
screenshots: 8
excerpt: "Chrome 离线安装包官方完整版下载地址。在线包和离线包的区别是什么？64位和32位怎么选？这篇文章一次讲清楚。"
card_icon: "📥"
card_label: "Chrome下载"
card_gradient: "#2a2210,#0d1117"
images: ["/images/download/chrome-offline-installer-download/cover.jpg"]
og_image: "/images/download/chrome-offline-installer-download/og.jpg"
keywords: "Chrome下载,Chrome离线安装包,Chrome完整版,Chrome安装教程,Chrome官方下载"
faq:
  - q: "Chrome 离线安装包下载教程：官方完整版地址 + 安装步骤详解安全吗？"
    a: "从官方渠道下载最安全。本站提供的下载链接均指向官方或可信来源，安装前建议核对文件数字签名。"
  - q: "下载后安装失败怎么办？"
    a: "检查安装包是否完整下载，关闭杀毒软件后重试，确保系统版本符合最低要求。如仍失败，尝试以管理员身份运行安装程序。"
  - q: "使用Chrome安全吗？"
    a: "正规渠道获取的软件是安全的。建议始终从官方下载，避免第三方修改版，并定期更新到最新版本。"
  - q: "支持哪些操作系统？"
    a: "通常支持 Windows 10/11，部分也支持 macOS 和 Linux。具体系统要求请查看本文的安装说明部分。"
  - q: "如何保持软件最新版本？"
    a: "大多数软件支持自动更新检查。也可以定期访问官网下载最新版本，或开启软件内的自动更新选项。"

---

你在网上搜"Chrome 下载"，找到的链接十有八九是"在线安装包"——一个不到 1MB 的小文件，双击后才开始真正下载 Chrome。问题是在国内网络环境下，这个在线下载经常中断、失败或超时。

这篇文章给你的是**官方离线安装包（Standalone Installer）**——下载下来就是一个完整的安装程序，不需要联网就能安装。

## 在线安装包 vs 离线安装包

先搞清楚两种安装包的区别：

| | 在线安装包 | 离线安装包 |
|--|----------|----------|
| 文件大小 | ~1MB | ~90MB（64位）/ ~80MB（32位） |
| 安装时需要联网？ | ✅ 需要 | ❌ 不需要 |
| 国内下载稳定性 | 容易中断 | 下载一次就行 |
| 安装速度 | 取决于网速 | 1 分钟内完成 |
| 适合场景 | 网络稳定时 | 网络不稳定 / 批量安装 / 系统重装后 |

**建议：** 如果你在国内，优先下载离线安装包。在线安装包在国内经常因为 Google 服务器被限制而下载失败。关于 <a href="/tips/chrome-common-problems-in-china/">Chrome 在国内使用的常见问题</a>我们也整理了详细的解决方案。

## Windows 版官方离线安装包下载地址

![#Windows 版官方离线安装包下载地](/images/download/chrome-offline-installer-download/body3.jpg)


以下链接均为 Google 官方服务器地址，直接点击即可下载。

### Windows 64 位（推荐）

如果你的电脑是 64 位系统（现在绝大多数电脑都是），选这个：

**最新稳定版：**
```
https://dl.google.com/chrome/install/latest/chrome_installer.exe
```

**特定版本（以 131.0.6778.86 为例）：**
```
https://dl.google.com/release2/chrome/AK64Y6NSU5HS6_131.0.6778.86/131.0.6778.86_chrome_installer.exe
```

> ⚠️ 特定版本的链接格式会随版本更新变化，建议使用"最新稳定版"链接，它始终指向当前最新版本。

### Windows 32 位

只有在使用老旧 32 位系统时才需要这个：

```
https://dl.google.com/chrome/install/latest/chrome_installer_32.exe
```

### macOS 版

Mac 用户通过在线方式或 Homebrew 安装更方便：

```bash
brew install --cask google-chrome
```

如果需要离线安装，可以从 https://www.google.com/chrome/ 下载 macOS 版安装包（dmg 格式，约 200MB）。

## 如何确认你的系统是 64 位还是 32 位

**Windows 10/11：** 右键"此电脑" → 属性 → 查看"系统类型"

如果显示"64 位操作系统, 基于 x64 的处理器"，下载 64 位版本。如果显示"32 位操作系统"，下载 32 位版本。

**Windows 7：** 开始 → 右键"计算机" → 属性 → 查看"系统类型"

> 2023 年的数据显示，全球 97% 以上的 Windows 电脑是 64 位系统。如果你不确定，选 64 位基本不会错。

## 安装前的系统要求

![#安装前的系统要求](/images/download/chrome-offline-installer-download/body2.jpg)


在下载之前，先确认你的电脑满足 Chrome 的最低运行要求：

**Windows 版：**
- Windows 10 或更高版本（Chrome 131 已停止支持 Windows 7/8/8.1）
- 处理器：x86 或 x64 架构
- 内存：至少 2GB（推荐 4GB 以上）
- 硬盘空间：至少 500MB（安装后约 400MB，加上缓存和数据约 1-2GB）
- 网络：安装本身不需要，但首次使用需要联网

**Mac 版：**
- macOS 11（Big Sur）或更高版本
- Apple Silicon（M1/M2/M3）和 Intel 芯片均支持
- 内存：至少 4GB
- 硬盘空间：至少 500MB

**如果你还在用 Windows 7：** Chrome 官方已不再提供 Windows 7 的新版本更新。最后一个支持 Windows 7 的版本是 Chrome 109（2023年1月发布）。如果必须使用，可以在博客园的教程中找到 Chrome 109 的离线安装包下载地址。但从安全角度，强烈建议升级到 Windows 10/11。

**Chrome 版本号含义：** Chrome 的版本号格式为 `主版本.次版本.构建号.补丁号`（如 131.0.6778.86）。对于普通用户，只需要关注主版本号（131）——大约每 4 周更新一次。次版本号和构建号由 Google 内部管理，用户无需关心。

## 安装步骤

### 第一步：下载离线安装包

点击上面的 64 位下载链接，浏览器会开始下载一个约 90MB 的 exe 文件。

**如果下载很慢：** 可以在下载工具（IDM、迅雷）中粘贴链接进行多线程下载，速度会快很多。也可以把链接粘贴到迅雷或 IDM 中，设置 16 线程下载，通常 1-2 分钟就能下完。

**下载后如何验证文件完整性：** 在命令提示符中运行 `certutil -hashfile chrome_installer.exe SHA256`，将输出的哈希值与 Google 官方公布的哈希值对比（可在 Chrome 发布日志中查到）。如果一致，说明文件没有被篡改。

### 第二步：关闭正在运行的 Chrome

如果电脑上已经安装了旧版 Chrome，安装前先完全退出 Chrome：
1. 关闭所有 Chrome 窗口
2. 检查系统托盘（右下角），如果 Chrome 图标还在，右键点击 → 退出
3. 打开任务管理器（Ctrl + Shift + Esc），确认没有 Chrome 相关进程
4. 如果任务管理器中有 Chrome 进程无法关闭，可以在命令提示符中运行 `taskkill /F /IM chrome.exe` 强制结束

### 第三步：运行安装程序

双击下载好的 `chrome_installer.exe`，会弹出用户账户控制（UAC）提示，点击"是"。

Chrome 会自动完成安装（约 30 秒），过程中不需要任何手动操作。安装路径默认为 `C:\Program Files\Google\Chrome\Application\`。如果你在安装过程中遇到问题，也可以参考 <a href="/tips/chrome-common-problems-in-china/">Chrome 国内使用常见问题</a>中的解决方案。

**安装过程中常见问题：**
- **提示"安装失败，错误代码 0x80004005"：** 通常是因为权限不足。右键点击安装包 → "以管理员身份运行"重试。
- **提示"请关闭所有 Google Chrome 窗口"：** 说明后台还有 Chrome 进程在运行。回到第二步，用任务管理器彻底关闭所有 Chrome 进程。
- **安装卡在"正在安装"不动：** 尝试结束安装进程后重新运行，或重启电脑后再安装。
- **杀毒软件拦截安装：** Chrome 官方安装包不会携带病毒。如果是 360、火绒等杀毒软件拦截，选择"允许安装"即可。

### 第四步：验证安装

安装完成后，Chrome 会自动启动。检查版本号：
1. 点击右上角三个点 → 帮助 → 关于 Google Chrome
2. 显示当前版本号即为安装成功
3. 如果页面显示"Chrome 已是最新版本"，说明安装正常

### 第五步：首次使用配置

Chrome 首次启动后，建议做以下基础配置：

1. **登录 Google 账号**：如果你有 Google 账号，登录后可以同步书签、密码和扩展。注意国内环境可能需要网络工具才能登录。
2. **设置默认浏览器**：Chrome 会弹出提示，点击"设为默认"。也可以手动设置：Windows 设置 → 应用 → 默认应用 → Web 浏览器 → Google Chrome。如果设置后被其他浏览器篡改，可以参考 <a href="/tips/chrome-default-browser/">Chrome 设为默认浏览器的完整教程</a>。
3. **设置默认搜索引擎**：chrome://settings/search → 如果 Google 搜索不可用，可以添加百度或 Bing 作为默认。详细的搜索引擎切换方法可以参考 <a href="/tips/chrome-search-engine-change/">Chrome 搜索引擎切换全攻略</a>。
4. **导入其他浏览器的数据**：Chrome → 设置 → 导入书签和设置 → 选择要导入的浏览器 → 勾选需要导入的数据（书签、密码、历史记录）。

## 企业批量安装（IT 管理员参考）

![#企业批量安装（IT 管理员参考）](/images/download/chrome-offline-installer-download/body1.jpg)


如果你是 IT 管理员，需要在多台电脑上批量安装 Chrome，可以使用以下方法：

**方法一：MSI 安装包**

Google 提供了 MSI 格式的安装包，支持静默安装和通过组策略管理：

```
https://dl.google.com/chrome/install/googlechromestandaloneenterprise64.msi
```

静默安装命令：
```
msiexec /i googlechromestandaloneenterprise64.msi /quiet /qn
```

**方法二：命令行静默安装**

使用 exe 安装包也可以静默安装：
```
chrome_installer.exe /silent /install
```

**方法三：配置策略模板**

安装 Chrome 企业版后，可以下载 Google Chrome 策略模板（ADMX），通过组策略管理 Chrome 的默认设置（主页、扩展白名单、代理设置等）。模板下载地址：https://chromeenterprise.google/policies/

## 不同渠道的 Chrome 版本区别

Chrome 有四个发布渠道，普通用户只需要关注稳定版：

| 渠道 | 更新频率 | 稳定性 | 适合谁 |
|------|---------|--------|-------|
| Stable（稳定版） | 每 4 周 | ⭐⭐⭐⭐⭐ | 所有用户 |
| Beta（测试版） | 每 周 | ⭐⭐⭐⭐ | 想提前体验新功能的用户 |
| Dev（开发版） | 每 周 | ⭐⭐⭐ | 开发者 |
| Canary（金丝雀版） | 每 天 | ⭐⭐ | Chrome 开发团队成员 |

本文提供的下载链接均为稳定版。如果你想安装 Beta 或 Dev 版，可以访问 https://www.google.com/chrome/beta/ 和 https://www.google.com/chrome/dev/。

**为什么不要用第三方下载站的 Chrome：** 国内很多软件下载站（如太平洋下载、华军软件园、非凡软件站等）提供的 Chrome 安装包被捆绑了广告软件、浏览器劫持工具或首页修改程序。即使安装包大小和官方一致，也可能被注入了额外代码。**只从 Google 官方链接下载是最安全的做法。** 如果你无法直接访问 Google 服务器，宁可找身边有条件的同事帮忙下载，也不要从未知网站下载。

## 常见问题

### 离线安装包下载链接打不开怎么办？

Google 的下载服务器（dl.google.com）在国内部分网络环境下访问不稳定。解决方案：使用代理工具下载；在下载工具（IDM、迅雷）中设置代理后粘贴链接下载；或从 GitHub 上的 chrome-offline-installer 项目获取镜像。如果都不可用，也可以搜索"Chrome 离线安装包"在第三方软件站下载（注意选择可信站点，下载后用杀毒软件扫描）。

### 覆盖安装会丢失书签和密码吗？

不会。Chrome 的用户数据（书签、密码、历史记录、扩展等）保存在 `C:\Users\<用户名>\AppData\Local\Google\Chrome\User Data\` 目录中，和安装目录是分开的。覆盖安装只会替换程序文件，不会影响用户数据。即使你先卸载再安装，只要不手动删除 User Data 目录，数据就不会丢失。

### 离线安装包和绿色免安装版怎么选？

离线安装包会自动创建快捷方式、注册系统服务、关联 HTML 文件，且支持自动更新——大多数用户应该选这个。绿色免安装版（Portable）解压即用、不写入注册表，但不会自动更新。适合需要把 Chrome 放在 U 盘里随身携带、或者在安装受限的电脑上临时使用的情况。

### 公司电脑没有管理员权限怎么办？

Chrome 默认安装到 `C:\Program Files\` 目录需要管理员权限。如果无法获取管理员权限，可以：联系 IT 部门安装企业版 MSI 包；或使用绿色免安装版解压到用户目录（如 `D:\Chrome\`），不需要管理员权限但不会自动更新。注意部分公司安全策略可能禁止运行未授权的浏览器，安装前先确认公司规定。

### 安装后怎么确认是纯净版（非篡改版）？

国内部分下载站会重新打包 Chrome 安装程序，加入推广软件或修改默认设置。验证方法：打开 chrome://settings/help 确认 Google 更新服务正常；打开 chrome://extensions/ 确认没有预装的可疑扩展；检查默认主页是否被篡改（应为 Google 首页或 Chrome 新标签页）；确认搜索引擎没有被锁定为某个国内搜索引擎。如果发现异常，建议卸载后从本文提供的官方链接重新下载。
