# _author: Coke
# _date: 2022/7/26 18:28

# 对 mock 相关 数据 进行初始化

import threading
import logging
import utils
import mock
import time


class MockHandler:
    """ 初始化 Mock 相关信息及配置 """

    def __init__(self):
        self._domain = [
            'www.baidu.com',
            'mitmproxy.org'
        ]
        self._port = 8888
        self._code_file = r'D:\PycharmProject\client-autotest-driver\test1.py'
        self.start_server()
        time.sleep(3)

    def start_server(self):
        """
        线程启动 mitmproxy 服务器
        :return:
        """
        _result = utils.usage_prot('127.0.0.1', self._port)
        if _result:
            logging.warning(f'端口: {self._port} 已被占用, 准备 kill 掉')
            utils.kill_prot(self._port)

        thread = threading.Thread(
            target=mock.start_mitmproxy_server,
            args=(self._code_file, self._port, self._domain),
            daemon=True
        )
        thread.start()


if __name__ == '__main__':
    MockHandler()
