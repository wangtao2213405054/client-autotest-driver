# _author: Coke
# _date: 2022/7/26 11:13

# 启动 mitmproxy 相关服务

import platform
import os


def start_mitmproxy_server(code_file, prot, domain_list):
    _filter = ' --ignore-hosts '
    _domain = ''

    _order = f'mitmdump -q -p {prot} -s {code_file}'
    # 不清楚什么原因 windows 上忽略是不生效的...
    if platform.system() == 'Darwin' or platform.system() == 'Linux':
        # add filter ...
        pass
    os.popen(_order)
