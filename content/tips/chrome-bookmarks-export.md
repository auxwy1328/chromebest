---
title: "Chrome 书签导出、导入与迁移完整教程：换浏览器、换电脑都能搞定"
date: 2026-05-30T10:00:00+08:00
slug: "chrome-bookmarks-export"
categories: ["使用技巧"]
tags: ["Chrome书签导出", "Chrome书签导入", "Chrome书签迁移", "Chrome换浏览器", "Chrome换电脑"]
description: "Chrome 书签导出、导入、迁移的完整教程：HTML/JSON 格式、多浏览器互导、Google 同步、换电脑书签迁移、书签丢失恢复方法。"
pinned: false
tag_icon: "📑"
tag_label: "书签管理"
tag_color: "teal"
readtime: 15
screenshots: 6
excerpt: "换浏览器怕丢书签？换电脑怕同步不了？这篇文章教你 Chrome 书签的导出、导入、迁移和恢复，覆盖所有主流浏览器和操作系统。"
card_icon: "📑"
card_label: "书签导出"
card_gradient: "#0d2e2e,#1a3a3a"
faq:
  - question: "Chrome 书签导出在哪里？"
    answer: "打开 Chrome 右上角三个点 → 书签和列表 → 书签管理器，在管理器中点击右上角三个点 → 导出书签。Chrome 会生成一个 HTML 格式的书签文件，几乎所有浏览器都能识别。另外，Chrome 的书签数据也保存在本地 JSON 文件中，路径为用户数据目录下的 Bookmarks 文件。"
  - question: "Chrome 书签能同步到另一台电脑吗？"
    answer: "可以。在两台电脑上都登录同一个 Google 账号并开启同步，书签会自动同步。但需要注意：如果两台电脑的书签不一致，Chrome 会尝试合并，可能导致重复书签。建议先在一台电脑上导出书签备份，然后再开启同步。另外，国内使用 Google 同步需要能访问 Google 服务，否则同步会失败。"
  - question: "Chrome 书签不小心全删了怎么恢复？"
    answer: "如果开启了 Google 同步，可以在 Google 网页版的书签管理中恢复。如果没开启同步，检查本地书签备份文件。Chrome 会在用户数据目录下自动创建 Bookmarks.bak 备份文件。Windows 路径为 C:\\Users\\用户名\\AppData\\Local\\Google\\Chrome\\User Data\\Default\\Bookmarks.bak。将 Bookmarks.bak 重命名为 Bookmarks 并重启 Chrome 即可恢复。"
  - question: "从 Firefox 迁移书签到 Chrome 最好的方法？"
    answer: "最简单的方法是安装 Chrome 的导入工具。Chrome 首次启动时会提示从其他浏览器导入，包括书签、密码、历史记录等。也可以手动操作：在 Firefox 中导出书签为 HTML 文件，然后在 Chrome 中导入。两种方法效果相同，但 Chrome 内置的导入工具还能同时迁移密码和扩展。"
  - question: "Chrome 书签导出的 HTML 文件和 JSON 文件有什么区别？"
    answer: "HTML 格式是通用格式，几乎所有浏览器都支持导入和导出，适合跨浏览器迁移。JSON 格式是 Chrome 内部使用的格式，包含书签的元数据（添加时间、文件夹结构等），适合精确恢复。日常迁移用 HTML 就够了。如果需要编辑书签或处理大量书签，JSON 格式更方便用脚本处理。"
---

换电脑的时候，最怕的不是重装系统，而是发现存了五年的书签全没了。换浏览器也一样，收藏了几百个网站的快捷入口，换过去一个都找不到。这种焦虑不是杞人忧天——我见过太多人因为没做书签备份，换设备后花了整整一周重新整理。

这篇文章把 [Chrome 浏览器](/) 的书签导出、导入、迁移和恢复全讲透了。不是那种只教你怎么点三个按钮的浅层教程，而是从文件格式到多浏览器互导、从同步机制到丢失恢复，所有环节都覆盖到的实操指南。

![一台旧电脑和一台新电脑之间流动书签数据的示意图，突出迁移场景](/images/tips/chrome-bookmarks-export/img1.jpg)

## 先搞清楚：Chrome 书签存在哪

知道书签的物理位置，才能真正做到心里有数。无论你是日常使用 [Chrome 浏览器](/) 还是准备做大规模数据迁移，这都值得了解。Chrome 的书签数据在两个地方：

**第一，用户数据目录（本地）。** Chrome 在本地用一个 JSON 文件存储所有书签。不同操作系统的路径不同：

- Windows：`C:\Users\用户名\AppData\Local\Google\Chrome\User Data\Default\Bookmarks`
- macOS：`~/Library/Application Support/Google/Chrome/Default/Bookmarks`
- Linux：`~/.config/google-chrome/Default/Bookmarks`

这个文件是 Chrome 的核心书签数据库。每次添加、删除、修改书签，Chrome 都会更新这个 JSON 文件。同时，Chrome 还会自动生成 `Bookmarks.bak` 备份文件，用于崩溃恢复。

**第二，Google 账号（云端）。** 如果你开启了 Chrome 同步，书签会通过 Google 账号同步到云端。登录同一个 Google 账号的任何设备都能获取这些书签。

这两个位置各有用途，后面会详细展开。现在先记住：本地 JSON 文件是你最后的底线，Google 同步是方便但有条件的远程备份。

## Chrome 书签的两种文件格式

在正式操作之前，必须搞清楚 Chrome 书签涉及的两种文件格式，否则后续操作容易踩坑。

### HTML 格式：跨浏览器迁移的通用语言

Chrome 书签管理器的导出功能生成的是 HTML 格式文件。这种格式从 Netscape Navigator 时代就有了，几乎所有浏览器都支持导入和导出。它本质上就是一个包含书签链接的网页文件，结构简单，用文本编辑器就能打开。

HTML 书签文件长这样：

```html
<DT><H3 ADD_DATE="1700000000" LAST_MODIFIED="1700000100">工作相关</H3>
<DL><p>
    <DT><A HREF="https://example.com" ADD_DATE="1700000000">示例网站</A>
    <DT><A HREF="https://another-site.com" ADD_DATE="1700000005">另一个网站</A>
</DL><p>
```

可以看到，HTML 格式保留了文件夹结构和基本的添加时间戳。但更详细的信息（比如书签图标 URL、访问次数）会被丢弃。

**HTML 格式适合的场景：** 跨浏览器迁移（Chrome 到 Firefox、Edge、Safari 等）、手动备份、导入到书签管理工具。

### JSON 格式：Chrome 的内部数据结构

Chrome 本地存储的 `Bookmarks` 文件是 JSON 格式。相比 HTML，JSON 包含了更丰富的元数据：

- `date_added`：精确到微秒的添加时间
- `date_last_used`：最后访问时间
- `icon_url`：网站图标 URL
- `meta_info`：页面的描述和标题缓存

JSON 格式不适合直接用于跨浏览器迁移，因为其他浏览器不一定能解析 Chrome 的 JSON 结构。但它是精确恢复和脚本批量处理的最佳选择。

**JSON 格式适合的场景：** 精确恢复书签、批量编辑书签（用 Python/Node.js 脚本）、从备份文件恢复。

### 什么时候用哪种？

| 场景 | 推荐格式 | 原因 |
|------|----------|------|
| 换浏览器 | HTML | 通用兼容性 |
| 手动备份 | HTML | 简单直观 |
| 脚本批量处理 | JSON | 结构化数据 |
| 精确恢复 | JSON | 保留完整元数据 |
| 长期存档 | 两者都存 | HTML 保通用，JSON 保完整 |

## Chrome 书签导出操作详解

### 方法一：通过书签管理器导出 HTML

这是最常用的导出方法，适合绝大多数场景。

1. 打开 Chrome，点击右上角三个点
2. 选择书签和列表 → 书签管理器（也可以直接按 `Ctrl+Shift+O`）
3. 在书签管理器中，点击右上角三个点（菜单按钮）
4. 选择导出书签
5. 选择保存位置，Chrome 会生成一个 `.html` 文件

![Chrome 书签管理器界面，标注右上角菜单按钮和导出书签选项](/images/tips/chrome-bookmarks-export/img2.jpg)

这个导出文件包含了你所有的书签和文件夹结构。默认文件名是 `bookmarks_年_月_日_时_分_秒.html`，方便你区分不同时间的备份。

注意几点：

- 导出的是全部书签，不支持选择性导出某个文件夹。如果你只想导出部分书签，需要导出后手动编辑 HTML 文件
- 导出的 HTML 文件不包含书签图标（favicon），只包含 URL 和名称
- 不会导出书签的访问历史和最后访问时间

### 方法二：直接复制 Bookmarks JSON 文件

如果你需要完整数据，直接去用户数据目录复制 `Bookmarks` 文件。

1. 关闭 Chrome（重要，否则文件可能被锁定或写入不一致）
2. 打开文件资源管理器，导航到 `C:\Users\你的用户名\AppData\Local\Google\Chrome\User Data\Default\`
3. 复制 `Bookmarks` 文件到安全位置
4. 如果 `Bookmarks.bak` 也存在，一并复制

这个方法的优势是数据完整，劣势是不能直接导入到其他浏览器。

### 方法三：使用 Google 网页版查看书签

如果你开启了 Chrome 同步，可以在任何设备的浏览器中访问 `https://www.google.com/bookmarks/` 查看你的书签。注意这个页面只能查看，不能导出。实际的书签管理在 Chrome 的同步设置中。

## Chrome 书签导入操作详解

### 导入 HTML 书签文件

1. 打开 Chrome 书签管理器（`Ctrl+Shift+O`）
2. 点击右上角三个点
3. 选择导入书签
4. 选择之前导出的 HTML 文件

![Chrome 书签管理器的导入书签对话框](/images/tips/chrome-bookmarks-export/img3.jpg)

导入后，Chrome 会在书签栏下方创建一个以 HTML 文件命名的文件夹（比如 Imported from bookmarks_2026_05_30.html），所有导入的书签都在这个文件夹中。

这意味着导入的书签不会自动融入你现有的书签结构。你需要手动将它们拖拽到合适的位置。

### 从其他浏览器自动导入

如果你刚安装 Chrome 或重新安装，首次启动时 Chrome 会提示是否从其他浏览器导入数据。这个导入功能比手动导入 HTML 更强大，因为可以同时导入：

- 书签
- 已保存的密码
- 浏览历史记录
- 浏览器扩展（部分支持）
- 自动填充表单数据
- 付款方式信息

如果你想手动触发这个导入：

1. 打开 Chrome 设置（`chrome://settings/`）
2. 搜索导入或点击左侧的「您和 Google」
3. 找到「从其他浏览器导入」选项

Chrome 能自动检测已安装的 Firefox、Edge、Safari、IE，并显示可导入的数据类型。这一点比 [Chrome 和 Firefox 的对比](/compare/chrome-vs-firefox-2026/) 中提到的迁移功能更具体——Chrome 对自家 Chromium 内核的 Edge 支持尤其好，能迁移的数据类型最多。

## 多浏览器互导完全方案

实际使用中，书签迁移不只是 Chrome 到 Chrome，更多是跨浏览器。下面给出所有主流浏览器之间的互导方案。

### Chrome 到 Firefox

**方案 A：Firefox 内置导入**
1. 打开 Firefox 设置 → 导入和备份 → 从另一个浏览器导入
2. 选择 Chrome，勾选书签
3. 完成导入

Firefox 的导入工具会直接读取 Chrome 的本地数据文件，不需要你先在 Chrome 中导出 HTML。

**方案 B：HTML 中转**
1. 在 Chrome 中导出书签为 HTML
2. 在 Firefox 中按 `Ctrl+Shift+O` 打开书签管理器
3. 点击导入和备份 → 从 HTML 导入书签
4. 选择 Chrome 导出的 HTML 文件

### Chrome 到 Edge

Edge 和 Chrome 都基于 Chromium 内核，迁移体验最顺畅。

**方案 A：Edge 首次启动导入**
1. 安装 Edge 后首次启动，选择从 Chrome 导入
2. 勾选书签及其他数据
3. 完成

**方案 B：Edge 设置导入**
1. 打开 Edge 设置（`edge://settings/`）
2. 侧边栏选择配置文件 → 导入浏览器数据
3. 选择 Chrome，勾选书签

**方案 C：直接复制用户数据**
这是最快但最野的方法。Chrome 和 Edge 的书签文件格式几乎相同。如果你胆大，可以直接把 Chrome 的 `Bookmarks` JSON 文件复制到 Edge 的用户数据目录。但我不推荐这个方法，因为版本差异可能导致数据结构不兼容。详细对比可以参考 [Chrome 和 Edge 的全面对比](/compare/chrome-vs-edge-2026/)。

### Chrome 到 Safari（macOS）

Safari 导入 Chrome 书签的最佳方式是通过 HTML 文件中转：

1. 在 Chrome 中导出书签为 HTML
2. 打开 Safari → 文件 → 导入自 → 书签 HTML 文件
3. 选择 Chrome 导出的 HTML 文件

Safari 导入后会创建一个名为 Imported Items 的文件夹。你可以手动整理到书签栏。

### Chrome 到其他浏览器（Brave、Vivaldi、Opera）

这些浏览器都基于 Chromium 内核，导入 Chrome 书签的方式和 Edge 类似——都在设置中提供从 Chrome 导入的选项。也都可以通过 HTML 文件导入。

**关键结论：** HTML 是书签迁移的万能中转格式。不管你想从哪个浏览器迁移到哪个浏览器，先导出 HTML 再导入，永远不会出问题。这比纠结选哪个浏览器更重要——毕竟 [Chrome 浏览器](/) 能做的事，大多浏览器也能做。

## Google 同步：方便但有限制

很多人以为开了 Chrome 同步就万事大吉了，实际上同步有好几个需要注意的地方。

### 同步的工作原理

开启 Google 同步后，Chrome 会把你所有的书签加密上传到 Google 服务器。在其他设备上登录同一个 Google 账号，书签就会自动下载。同步频率大约是实时到几分钟不等，取决于网络状况。

### 同步的优势

- **零操作迁移**：新电脑上登录 Chrome 就能获取所有书签，不需要手动导出导入
- **多设备一致性**：在公司电脑添加的书签，回家电脑上也能看到
- **丢失可恢复**：即使电脑坏了，书签还在 Google 服务器上

### 同步的风险和限制

**第一，网络依赖。** 国内用户需要能访问 Google 服务才能同步。如果你的网络环境不稳定，同步可能失败甚至丢失数据。Chrome 在同步失败时通常不会给出明显的错误提示，你可能在不知不觉中丢失了最新添加的书签。

**第二，合并冲突。** 如果两台电脑上的书签不一致（比如各自独立添加了一些书签），Chrome 的合并算法有时会产生重复书签。这在长期不同步的设备上尤其常见。

**第三，删除同步。** 在一台设备上删除书签，同步后会在所有设备上删除。这不是撤销操作——如果你在另一台电脑上等着那个书签回来，不会发生的。

**第四，数据量限制。** Google 同步书签有数量上限（约几万个），超过后同步可能会失败。对于重度书签用户（收藏了几千个页面的），需要注意这个限制。

### 同步 vs 手动导出：怎么选？

| 维度 | Google 同步 | 手动导出 |
|------|-----------|----------|
| 便利性 | 高，自动完成 | 低，需要手动操作 |
| 可靠性 | 中，依赖网络和 Google 服务 | 高，文件在你手上 |
| 数据完整性 | 高，包含所有元数据 | HTML 导出丢失部分信息 |
| 安全性 | 中，数据在 Google 服务器 | 高，本地文件 |
| 适用场景 | 日常多设备使用 | 换电脑、备份、跨浏览器 |

**我的建议是：两者都做。** 日常使用靠同步保持多设备一致，定期（每月一次）手动导出 HTML 文件作为备份。这样即使 Google 账号出问题或者同步故障，你还有本地备份兜底。

![一个对比表格展示 Google 同步和手动导出的优劣势，用图标区分](/images/tips/chrome-bookmarks-export/img4.jpg)

## 换电脑时的完整迁移流程

换电脑是书签迁移需求最强烈的场景。不只是书签，你可能还想把密码、扩展、设置一起迁过去。下面是完整的换电脑流程。

### 第一步：旧电脑上导出所有数据

在旧电脑上做以下操作：

1. **导出书签**：按前面说的方式导出 HTML 书签文件，复制 `Bookmarks.bak` JSON 文件
2. **导出密码**：Chrome 设置 → 密码和自动填充 → Google 密码管理器 → 导出密码（导出为 CSV 文件）。如果你还不知道怎么管理 Chrome 密码，可以看看 [Chrome 查看保存的密码的方法](/tips/chrome-password-view/)
3. **记录扩展列表**：打开 `chrome://extensions/`，截图或手动记录已安装的扩展。Chrome 同步会同步扩展，但有些需要重新配置。关于哪些扩展值得装，参考 [Chrome 必备扩展推荐](/plugins/chrome-essential-extensions/)
4. **导出其他数据**（可选）：浏览历史记录、自动填充数据等

把这些文件都保存到 U 盘或云盘。

### 第二步：新电脑上安装 Chrome

先下载 Chrome 安装包。如果你在新电脑上网络不稳定，建议下载 [Chrome 离线安装包](/download/chrome-offline-installer/)，避免在线安装失败。

安装后，有两种迁移路径：

**路径 A：Google 同步迁移（推荐）**
1. 启动 Chrome，登录旧电脑上使用的 Google 账号
2. 开启同步，等待书签、密码、扩展自动同步
3. 同步完成后，检查是否有遗漏或重复

**路径 B：手动导入迁移（同步不可用时的备选）**
1. 启动 Chrome，先不登录或登录后关闭同步
2. 打开书签管理器，导入 HTML 书签文件
3. 打开密码设置，导入 CSV 密码文件
4. 重新安装需要的扩展

### 第三步：验证和整理

迁移完成后，逐项检查：

- 书签数量是否和旧电脑一致（在书签管理器中数文件夹和条目）
- 书签栏的书签是否都在
- 文件夹结构是否完整
- 密码数量是否匹配
- 扩展是否全部就位

如果使用 Google 同步迁移，重点关注是否有重复书签。Chrome 的合并算法偶尔会产生重复，需要手动清理。

### 不只是书签：完整浏览器数据迁移

如果你想把整个 Chrome 搬过去（包括所有设置、缓存、Cookie、扩展配置），可以复制整个 Chrome 用户数据目录：

- Windows：`C:\Users\用户名\AppData\Local\Google\Chrome\User Data\`
- macOS：`~/Library/Application Support/Google/Chrome/`
- Linux：`~/.config/google-chrome/`

把这个目录整个复制到新电脑的相同位置。注意需要关闭 Chrome 再复制，否则文件可能被锁定。这个方法虽然粗暴但最完整，相当于把旧电脑的 Chrome 原封不动搬过来了。

## 书签整理技巧

迁移书签的同时，也是整理书签的好时机。很多人积累了上千个书签却从来不整理，最后变成一个无法使用的垃圾堆。

### 书签栏 vs 其他书签

Chrome 把书签分为三个区域：

- **书签栏**：显示在地址栏下方的常用书签，适合放高频访问的网站
- **其他书签**：不常访问的书签，折叠在书签菜单中
- **移动设备书签**：专为手机设计的书签文件夹

建议的使用方式：书签栏只放 10-15 个最高频的网站，超过这个数量会显得拥挤且不好找。其他书签按主题分文件夹管理。

### 文件夹管理策略

不要创建超过三层的文件夹嵌套。超过三层后，找书签的时间比重新搜索还长。

推荐的结构：

```
书签栏
├── 工作
│   ├── 项目文档
│   └── 协作工具
├── 学习
│   ├── 教程
│   └── 文档参考
└── 日常
    ├── 社交媒体
    └── 购物

其他书签
├── 待读文章
├── 参考资料
├── 工具网站
└── 归档（按季度或年份）
```

关键原则：**定期清理比定期整理更重要。** 每季度花 10 分钟删除不再需要的书签，比花两小时重新分类几百个书签效率高得多。

### 批量编辑书签

Chrome 自带的书签管理器只支持基本的搜索和删除，不支持批量编辑。如果你需要批量修改书签（比如批量修改 URL、重命名、移动到新文件夹），有几种方法：

**方法一：编辑 HTML 书签文件。** 用文本编辑器打开导出的 HTML 文件，用查找替换功能批量修改。这种方法适合简单的 URL 替换（比如域名变更）。

**方法二：用脚本处理 JSON。** 用 Python 读取 Chrome 的 `Bookmarks` JSON 文件，批量处理后写回。这种方法适合复杂的编辑操作。

```python
import json

# 读取书签文件
with open('Bookmarks', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 递归遍历书签节点
def process_node(node):
    if node.get('type') == 'url':
        url = node.get('url', '')
        # 示例：将旧域名替换为新域名
        if 'old-site.com' in url:
            node['url'] = url.replace('old-site.com', 'new-site.com')
    children = node.get('children', [])
    for child in children:
        process_node(child)

# 处理所有根节点
for key in ['bookmark_bar', 'other', 'synced']:
    if key in data['roots']:
        process_node(data['roots'][key])

# 写回文件（先备份原文件！）
with open('Bookmarks_new', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=3)
```

**方法二：第三方工具。** Chrome 网上应用店中有一些书签管理扩展，支持批量编辑功能。比如 Bookmark Checker 可以批量检测死链，Transmute 可以在浏览器之间转换书签格式。

![展示一个组织良好的 Chrome 书签栏，文件夹结构清晰、分类明确](/images/tips/chrome-bookmarks-export/img5.jpg)

## 书签丢失后的恢复方法

这是很多人最害怕的情况——打开 Chrome 发现书签全没了。别慌，按下面的步骤排查和恢复。

### 情况一：开启了 Google 同步

如果你的 Chrome 开启了同步，恢复相对简单：

1. 打开 Chrome，确认已登录 Google 账号
2. 检查同步状态（`chrome://sync-internals/`）
3. 如果同步正常，等待几分钟后书签应该自动恢复
4. 如果同步状态异常，尝试在设置中关闭再重新开启同步
5. 访问 `https://www.google.com/bookmarks/` 确认云端书签是否存在

### 情况二：没有开启同步

如果你没有开启同步，但本地还有备份文件，可以恢复：

**恢复步骤：**

1. **完全关闭 Chrome**（任务管理器中确认没有 chrome.exe 进程）
2. 打开文件资源管理器，导航到用户数据目录
3. 找到 `Bookmarks.bak` 文件（这是 Chrome 自动创建的备份）
4. 将 `Bookmarks` 重命名为 `Bookmarks.corrupted`（保留作为备份）
5. 将 `Bookmarks.bak` 复制一份并重命名为 `Bookmarks`
6. 重新启动 Chrome，检查书签是否恢复

如果 `Bookmarks.bak` 也不存在或者也是空的，还可以尝试从系统备份恢复。Windows 的文件历史记录或第三方的备份软件可能保存了早期的 `Bookmarks` 文件。

### 情况三：同步和备份都没有

这是最糟糕的情况。如果既没有 Google 同步，本地备份文件也丢失了，恢复的可能性很小。但还有几个方法可以尝试：

- 检查 Windows 的文件历史记录或系统还原点
- 使用数据恢复软件扫描硬盘（Recuva 等），搜索 `.html` 或 `Bookmarks` 相关文件
- 检查云盘或 U 盘中是否有之前手动导出的书签文件
- 如果书签丢失是因为 Chrome 崩溃或更新，检查 `User Data\Default` 目录下是否有 `Bookmarks.202x-xx-xx` 格式的旧版本文件

## 书签同步的常见问题排查

### 同步后书签变少或变多

这种情况通常是同步合并冲突导致的。Chrome 在合并两份不一致的书签时，可能会产生重复条目，也可能覆盖掉一方的新增书签。

解决方案：手动对比两份书签，删除重复项。使用书签管理器的搜索功能，按 URL 查找重复书签。

### 书签同步后文件夹结构混乱

同步后的文件夹结构可能和预期不一致。这通常是因为不同设备上的书签经历了不同的修改，Chrome 的合并算法无法完美处理所有情况。

解决方案：在书签管理器中手动重新组织文件夹。这很耗时，但比每次同步后都出问题要好。

### 国内用户同步失败

Chrome 同步依赖 Google 服务，国内网络环境下经常失败。如果遇到同步问题：

- 确认网络能访问 Google 服务
- 检查代理设置是否正确配置
- 查看 `chrome://sync-internals/` 中的同步状态和错误信息
- 如果同步确实不可用，改为手动导出导入方式

手动导出虽然麻烦一些，但不依赖网络环境，对于 [Chrome 通知设置](/tips/chrome-notification-settings/) 这类个人偏好配置也建议手动记录。

## 不同操作系统的特殊注意事项

### Windows

Windows 上的 Chrome 书签路径已经提到过。额外注意几点：

- `AppData` 是隐藏文件夹，需要在文件资源管理器中开启显示隐藏文件才能看到
- 如果安装了多个 Chrome 配置文件（Profile），书签路径会变成 `User Data\Profile 1\`、`Profile 2\` 等
- 企业版 Chrome（Chrome Enterprise）的用户数据目录可能不同

### macOS

macOS 上的书签路径是 `~/Library/Application Support/Google/Chrome/Default/Bookmarks`。`Library` 文件夹在 Finder 中默认隐藏。

显示隐藏文件的方法：在 Finder 中按 `Cmd+Shift+.`

### Linux

Linux 上的路径是 `~/.config/google-chrome/Default/Bookmarks`。如果你使用的是 Chromium 而不是 Chrome，路径是 `~/.config/chromium/Default/Bookmarks`。

Chrome 用户数据目录在不同发行版上位置一致，因为都遵循 XDG 规范。

## 书签备份的最佳实践

最后一部分，聊聊长期的书签备份策略。很多人迁移书签是一次性需求，但日常备份同样重要。

### 自动备份方案

**方案一：定期手动导出 HTML**

最简单但容易忘记。设置日历提醒，每月导出一次 HTML 文件到云盘。

**方案二：脚本自动备份**

写一个定时脚本，每月自动复制 `Bookmarks` 和 `Bookmarks.bak` 到备份目录：

```powershell
# bookmarks-backup.ps1
$source = "$env:LOCALAPPDATA\Google\Chrome\User Data\Default\Bookmarks*"
$dest = "D:\Backups\ChromeBookmarks\$(Get-Date -Format 'yyyy-MM-dd')"
New-Item -ItemType Directory -Path $dest -Force | Out-Null
Copy-Item $source $dest -Force
Write-Output "Backup completed at $(Get-Date)"
```

用 Windows 任务计划程序每月自动执行这个脚本。

**方案三：Git 版本控制**

如果你是技术用户，可以把书签文件纳入 Git 管理。每次修改书签后 commit 一次，这样不仅备份了数据，还能追踪修改历史。

### 备份文件管理

备份文件也需要管理。建议：

- 每次备份文件名包含日期，方便区分版本
- 保留最近 6 个月的备份，更早的可以归档
- 至少保留一份在非本地存储（云盘、NAS、外部硬盘）

## 总结

Chrome 书签管理看起来简单，但涉及的细节比大多数人想象的多。核心要点回顾：

- 书签导出分 HTML（通用）和 JSON（精确）两种格式，跨浏览器迁移用 HTML，脚本处理用 JSON
- 多浏览器互导的最佳方案是 HTML 中转，几乎所有浏览器都支持
- Google 同步方便但有网络依赖和合并冲突风险，国内用户尤其需要注意
- 换电脑时同步和手动导出都要做，互为补充
- 书签丢失后优先从 `Bookmarks.bak` 恢复，其次检查 Google 同步和系统备份
- 养成定期备份书签的习惯，手动导出或脚本自动备份都可以

书签本质上是你个人互联网使用历史的索引。花点时间管理它，比你想象的有价值得多。如果你的 [Chrome 缓存占用过大](/tips/chrome-clear-cache/) 或者正在考虑 [把 Chrome 设为默认浏览器](/tips/chrome-default-browser/) 或者刚下载了 [Chrome 离线安装包](/download/chrome-offline-installer/) 准备迁移，建议先把现有书签备份好再操作。准备工作做充分了，后续迁移才会顺利。
