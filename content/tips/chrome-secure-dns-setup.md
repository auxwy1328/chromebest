---
title: "Chrome 安全 DNS 设置教程：提升浏览安全性和解析速度"
date: 2026-05-06T03:00:00+08:00
slug: "chrome-secure-dns-setup"
categories: ["使用技巧"]
tags: ["Chrome安全DNS", "Chrome DNS设置", "Chrome DoH", "DNS加密", "Chrome网络设置"]
description: "Chrome 安全 DNS（DNS over HTTPS）设置教程。什么是安全 DNS，为什么国内用户应该关闭它，以及如何选择合适的 DNS 服务。"
pinned: false
tag_icon: "🔒"
tag_label: "DNS设置"
tag_color: "blue"
readtime: 8
screenshots: 6
excerpt: "Chrome 安全 DNS 听起来很安全，但国内用户开启后反而可能变慢。这篇文章告诉你该不该开、怎么选 DNS 服务。"
card_icon: "🔒"
card_label: "安全DNS"
card_gradient: "#1a1a2e,#0d1117"
images: ["/images/chrome-dns/cover.jpg"]
keywords: "Chrome安全DNS,Chrome DNS设置,DNS over HTTPS,Chrome DoH,加密DNS"
---

Chrome 从版本 78 开始支持"安全 DNS"功能（也叫 DNS over HTTPS，简称 DoH）。这个功能推出后在隐私保护领域引起了很大讨论——支持者认为它增强了对 ISP 监控的防御，反对者认为它把 DNS 查询权从 ISP 转移到了少数几家大型科技公司手中。这个功能听起来很好——加密 DNS 查询防止被窃听——但对国内用户来说，开启它反而可能导致网页加载变慢。

这篇文章解释安全 DNS 的原理、国内用户的使用建议，以及如何选择合适的 DNS 服务。

## 什么是安全 DNS

**正常 DNS 查询：** 当你在浏览器地址栏中输入 `www.taobao.com` 并按下回车时，浏览器实际上需要知道这个域名对应的服务器 IP 地址（比如 `140.205.220.96`）。这个过程叫做 DNS 解析（Domain Name System）。这个查询过程通常是明文传输的（使用 UDP 协议的 53 端口）——意味着你的网络服务商（ISP）和同一个 Wi-Fi 网络中的其他人理论上可以看到你查询了哪些域名。

**安全 DNS（DoH）：** 使用 HTTPS 协议加密 DNS 查询。查询过程通过加密通道传输，ISP 和中间人看不到你查询了什么域名。

**另一种加密 DNS（DoT）：** DNS over TLS，使用 TLS 协议加密 DNS 查询。和 DoH 功能类似，但加密层级不同。Chrome 支持的是 DoH。

## 国内用户要不要开启安全 DNS

**结论：建议关闭。**

原因：
1. **速度变慢**：Chrome 默认的安全 DNS 服务器由 Google 和 Cloudflare 提供，都在国外。国内用户每次 DNS 查询都要绕到国外服务器，增加延迟（正常情况下 DNS 查询只需 10-50ms，使用国外的 DoH 服务器则可能需要 200-500ms）
2. **安全性提升有限**：ISP 能看到你访问了哪些网站（通过 IP 地址），即使 DNS 查询被加密了。安全 DNS 只隐藏了"你查询了什么域名"，不隐藏"你访问了什么 IP"
3. **国内 DNS 服务已经够用**：运营商提供的 DNS 和国内公共 DNS（如阿里 DNS、腾讯 DNS）已经足够快和安全

## 如何设置安全 DNS

### 关闭安全 DNS（国内用户推荐）

chrome://settings/security → 安全浏览 → 关闭"使用安全 DNS"

关闭后 Chrome 会使用系统默认的 DNS 服务器（通常是你宽带运营商自动分配的 DNS）。

### 开启安全 DNS（海外用户或需要隐私保护的用户）

chrome://settings/security → 安全浏览 → 开启"使用安全 DNS"→ 选择提供商

**推荐的 DoH 服务商：**

| 服务商 | 地址 | 特点 |
|--------|------|------|
| Cloudflare | `https://cloudflare-dns.com/dns-query` | 隐私保护好、全球节点多、速度快 |
| Google | `https://dns.google/dns-query` | 稳定可靠、全球覆盖 |
| Quad9 | `https://dns.quad9.net/dns-query` | 自带恶意域名过滤 |
| 阿里 DNS DoH | `https://dns.alidns.com/dns-query` | 国内访问快 |
| 腾讯 DNSPod DoH | `https://doh.pub/dns-query` | 国内访问快 |

**海外用户推荐 Cloudflare 或 Google。国内用户如果一定要用 DoH，选阿里 DNS 或腾讯 DNSPod。**

### 使用自定义 DoH 服务器

如果你选择的 DoH 服务商不在 Chrome 的下拉列表中，可以通过自定义方式添加：

1. 在"使用安全 DNS"下方选择"使用"→ 选择"自定义"
2. 在"自定义 DNS over HTTPS 服务器"中输入 DoH 服务器的 URL
3. 点击"确定"保存

## 系统 DNS 设置（和 Chrome 安全 DNS 是独立的）

Chrome 安全 DNS 只影响 Chrome 浏览器的 DNS 查询，不影响系统其他程序的 DNS。如果你想让所有程序都使用指定的 DNS，需要在操作系统中设置。

### Windows DNS 设置

1. 打开 Windows 设置 → 网络和 Internet → 点击你当前使用的网络连接（以太网或 Wi-Fi）→ DNS 服务器分配 → 点击"编辑"按钮
2. 在弹出面板中选择"手动"模式
3. 在"首选 DNS"和"备用 DNS"输入框中分别填入 DNS 服务器地址

**推荐的国内公共 DNS：**

| 服务商 | 首选 DNS | 备用 DNS | 特点 |
|--------|---------|---------|------|
| 阿里 DNS | 223.5.5.5 | 223.6.6.6 | 速度快、稳定 |
| 腾讯 DNSPod | 119.29.29.29 | 182.254.116.116 | 速度快、支持 DoH/DoT |
| 114 DNS | 114.114.114.114 | 114.114.115.115 | 老牌、稳定 |
| 百度 DNS | 180.76.76.76 | — | 简单 |

### 验证 DNS 设置是否生效

在命令提示符中运行：
```
nslookup www.taobao.com
```
查看返回的 DNS 服务器地址是否是你设置的 DNS 服务器。

## DNS 缓存和刷新

### Chrome DNS 缓存

Chrome 会缓存 DNS 查询结果以减少重复查询、加快页面加载速度。缓存中的每条记录都有一个 TTL（生存时间），过期后 Chrome 会重新查询。查看 Chrome 的 DNS 缓存：
1. 访问 chrome://net-internals/#dns
2. 在"Host cache"部分可以看到所有缓存的 DNS 记录

清除 Chrome DNS 缓存：点击"Clear host cache"按钮。

### 系统 DNS 缓存

Windows 操作系统也会缓存 DNS 查询结果（和 Chrome 的缓存是独立的）。清除系统 DNS 缓存的命令：
```
ipconfig /flushdns
```

**什么时候需要刷新 DNS 缓存：** 网站迁移服务器后旧 IP 被缓存导致浏览器仍然访问旧服务器无法打开新网站；遭遇 DNS 劫持或 DNS 污染导致搜索被重定向到广告页面；修改了 DNS 设置后需要让新设置立即生效（而不是等待旧缓存自动过期）。


## 国内 DNS 环境的特殊问题

国内 DNS 环境有一些特殊问题需要了解：

### DNS 污染

DNS 污染是指在网络传输过程中，DNS 查询的响应被篡改，返回错误的 IP 地址。常见的表现是访问 Google、YouTube 等网站时被跳转到其他页面，或者某些正常的域名解析失败。DNS 污染在国内是一个已知的存在，但普通用户不需要过于担心——它主要影响的是无法直接访问的网站。

### DNS 劫持

DNS 劫持比污染更恶劣——通常是运营商在 DNS 查询中注入广告或跳转。表现是访问一个不存在的域名时，浏览器会被跳转到运营商的广告页面或导航网站。解决办法：使用可信的公共 DNS（如阿里 DNS 223.5.5.5）替代运营商自动分配的 DNS。

### CDN 和 DNS 的关系

大型网站（如淘宝、B站、知乎）使用 CDN（内容分发网络）来加速访问。CDN 会根据你的地理位置返回最近的节点 IP。这意味着不同地区的用户即使使用同一个 DNS 服务器，解析到的 IP 地址也可能不同。使用公共 DNS 不会影响 CDN 的智能调度——CDN 是基于 DNS 查询的来源 IP 来判断地理位置的。

## 如何判断你的 DNS 是否正常工作

有时候网页打不开、加载慢或跳转到奇怪页面，可能是 DNS 出了问题。以下是排查方法：

**第一步：用 nslookup 测试 DNS 解析**

在命令提示符中运行 `nslookup www.baidu.com`，如果返回了正确的 IP 地址（如 `39.156.66.10` 或 `110.242.68.66`），说明 DNS 解析正常。如果返回"DNS request timed out"或错误的 IP，说明 DNS 有问题。

**第二步：用 ping 测试连通性**

如果 DNS 解析正常但网页打不开，可能是网络连接问题。运行 `ping www.baidu.com`，如果能收到回复（显示时间和 TTL），说明网络连通性正常。

**第三步：尝试切换 DNS**

如果 DNS 解析失败，尝试切换到公共 DNS（如阿里 DNS 223.5.5.5），然后再次运行 nslookup 测试。如果切换后正常了，说明之前的 DNS 服务器有问题。

**第四步：清除 DNS 缓存**

如果切换 DNS 后仍然有问题，可能是本地缓存了错误的 DNS 记录。运行 `ipconfig /flushdns` 清除系统 DNS 缓存，同时在 Chrome 中访问 `chrome://net-internals/#dns` 清除 Chrome DNS 缓存。

**第五步：重置网络设置**

如果以上步骤都无法解决问题，可以在 Windows 设置 → 网络和 Internet → 高级网络设置 → 网络重置 中重置网络适配器。这会清除所有的网络适配器配置（包括 DNS 设置、代理服务器配置、VPN 连接信息等），恢复到 Windows 的默认出厂网络状态。
## 常见问题

### 安全 DNS 能防止 DNS 污染吗？

部分可以。DNS 污染是指恶意方篡改 DNS 查询结果，让你访问到错误的 IP 地址。安全 DNS 通过加密通道发送查询请求，中间人无法篡改。但如果污染发生在 DNS 服务器端（比如返回了错误的 IP），安全 DNS 也无法防止。这种情况需要改用可信的 DNS 服务器来解决。

### 为什么有时候修改了 DNS 但没生效？

可能是 DNS 缓存还没过期。按以下顺序刷新：先清除 Chrome DNS 缓存（chrome://net-internals/#dns）→ 再清除系统 DNS 缓存（ipconfig /flushdns）→ 最后重启浏览器。如果仍然没有生效，可能需要等待 DNS 记录的 TTL（生存时间）自动过期后被清除，最长可能需要等待 48 小时（大部分 DNS 记录的 TTL 为 300 秒到 86400 秒不等）。

### 安全 DNS 和 VPN 有什么区别？

安全 DNS 只加密了 DNS 查询这一步（隐藏了"你想访问哪个域名"），但实际的网页访问过程（你和网站服务器之间的数据传输）仍然是明文的。VPN 则加密了所有网络流量（包括 DNS 查询和实际的网页数据传输），提供的是端到端的隐私保护。VPN 的隐私保护远强于安全 DNS。但如果只是想在 DNS 层面增加一些隐私保护，安全 DNS 比 VPN 轻量得多（不影响网速，不增加额外费用）。

### 使用公共 DNS 安全吗？

国内主流的公共 DNS（如阿里 DNS、腾讯 DNSPod、114 DNS 等）均由大型互联网公司或专业 DNS 服务商运营，安全性和可靠性都有保障。但理论上，任何公共 DNS 的运营者都能看到你查询了哪些域名。如果你非常在意隐私，可以自己搭建 DNS 服务器（使用 Pi-hole 或 AdGuard Home），完全控制 DNS 查询日志。不过这需要一台常开的服务器（如家用 NAS 或树莓派）和一定的网络配置知识，技术门槛相对较高，更适合有一定技术能力的网络爱好者或家庭实验室用户。

### Chrome 安全 DNS 和系统 DNS 哪个优先？

Chrome 安全 DNS 优先于系统 DNS。当 Chrome 的安全 DNS 功能开启时，Chrome 不会使用系统设置的 DNS 服务器，而是使用你指定的 DoH 服务器。这意味着：即使你在 Windows 中设置了阿里 DNS，Chrome 仍然会使用 Cloudflare 或其他 DoH 服务器。只有关闭 Chrome 安全 DNS 后，Chrome 才会使用系统 DNS。
