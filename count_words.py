# -*- coding: utf-8 -*-
import re

files = [
    r'C:\Projects\chromebest\content\tips\chrome-update-failed-fix.md',
    r'C:\Projects\chromebest\content\tips\chrome-sync-settings-guide.md',
]

for f in files:
    text = open(f, 'r', encoding='utf-8').read()
    body = text.split('---')[2]
    cc = len(re.findall(r'[\u4e00-\u9fff]', body))
    faq = len(re.findall(r'### ', body))
    print(f'{f.split(chr(92))[-1]}: {cc} chars, {faq} FAQ')
