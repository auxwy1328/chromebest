# -*- coding: utf-8 -*-
import re

f = r'C:\Projects\chromebest\content\tips\chrome-set-default-browser-guide.md'
text = open(f, 'r', encoding='utf-8').read()
body = text.split('---')[2]
cc = len(re.findall(r'[\u4e00-\u9fff]', body))
faq = len(re.findall(r'### ', body))
print(f'Chinese chars: {cc}')
print(f'FAQ count: {faq}')
