
import re
import mitmproxy
_re = r''

data = """
    https://example.com
    https://www.baidu.com:443
"""
print(re.findall('\D+baidu\.com:.+', data))
