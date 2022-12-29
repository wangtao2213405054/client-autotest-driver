# _author: Coke
# _date: 2022/7/26 11:13

# 启动 mitmproxy 相关服务

import multiprocessing
import platform
import logging
import os
import re


class MitmproxyProcess(multiprocessing.Process):
    """
    启动一个 mitmproxy 服务
    windows: windows 文件不会进行过滤
    mac: mac 会将所有非项目域名的请求过滤, 并且手机可以访问 apple 相关的域名, 防止安装 webdriver agent 导致无法信任的问题
    在 windows 中需要安装 mitmproxy 8.x 以上的版本
    mac 中则需要安装 6.0.2 版本的 mitmproxy 7.x以上的版本无法过滤域名
    """

    def __init__(self, code_file, port, domain_list, **kwargs):
        """
        初始化子进程
        :param code_file: mitmdump 指定脚本文件路径
        :param prot: mitmproxy 端口
        :param domain_list: 监听的域名列表
        :param kwargs: multiprocessing.Process 所需的参数
        """
        self.code_file = code_file
        self.port = port
        self.domain_list = domain_list
        super(MitmproxyProcess, self).__init__(**kwargs)

    def run(self) -> None:
        """
        重写 multiprocessing.Process 执行器
        :return:
        """
        _order = f'mitmdump -p {self.port} -q -s {self.code_file}'

        if platform.system() == 'Darwin':
            _re = map(lambda x: re.sub(r'\.', r'\.', x), self.domain_list)
            _re = map(lambda x: f'(?!{x}:)', _re)
            _domain = ''.join(_re)
            _filter = rf" --ignore-hosts '^(?![0-9\.]+:){_domain}'"
            _order += _filter

        logging.debug(f'准备启动 mitmproxy 服务器, 端口: {self.port}')
        logging.debug(f'启动命令: {_order}')
        os.system(_order)


if __name__ == '__main__':
    data_list = [
        'www.baidu.com',
        'mitmproxy.org'
    ]
