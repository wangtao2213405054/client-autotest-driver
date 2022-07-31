# _author: Coke
# _date: 2022/7/26 11:13

# 启动 mitmproxy 相关服务

import platform
import os
import re


def start_mitmproxy_server(code_file, prot, domain_list):
    """
    启动一个 mitmproxy 服务
    windows: windows 文件不会进行过滤
    mac: mac 会将所有非项目域名的请求过滤, 并且手机可以访问 apple 相关的域名, 防止安装 webdriver agent 导致无法信任的问题
    在 windows 中需要安装 mitmproxy 8.x 以上的版本
    mac 中则需要安装 6.0.2 版本的 mitmproxy 7.x以上的版本无法过滤域名
    """

    _order = f'mitmdump -p {prot} -q -s {code_file}'

    if platform.system() == 'Darwin' or platform.system() == 'Linux':

        _re = map(lambda x: re.sub(r'\.', r'\.', x), domain_list)
        _re = map(lambda x: f'(?!{x}:)', _re)
        _domain = ''.join(_re)
        _filter = rf" --ignore-hosts '^(?![0-9\.]+:){_domain}'"
        _order += _filter

    os.popen(_order)


if __name__ == '__main__':
    data_list = [
        'www.baidu.com',
        'mitmproxy.org'
    ]
    start_mitmproxy_server(r'D:\PycharmProject\client-autotest-driver\test1.py', 8888, data_list)
