import re

data_list = [
    'www.baidu.com',
    'www.mitmproxy.org',
    'www.info.com',
    'www.github.cn',
]


data = map(lambda x: re.sub(r'\.', r'\.', x), data_list)
data = list(map(lambda x: f'(?!{x}:)', data))
print(data)