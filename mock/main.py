# _author: Coke
# _date: 2022/7/26 18:28

# 对 mock 相关 数据 进行初始化

import threading
import logging
import utils
import mock


class MockHandler:
    """
    mock 服务主入口
    依赖于 mitmproxy
    """

    def __init__(self, prot):
        """
        初始化 Mock 相关信息及配置
        :param prot: 要启动的端口号
        """
        self._port = prot
        self._domain = self.get_domain
        self._api = self.get_api
        self._code_file = mock.CreateMockCode(self._api).create_file()
        self.start_server()

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

    @property
    def get_domain(self):
        """
        获取当前项目下的域名列表
        mock data
        """
        _domain = [
            'www.baidu.com',
            'mitmproxy.org',
            'python.org',
            'github.org'
        ]
        return _domain

    @property
    def get_api(self):
        """
        获取当前项目下的所有接口
        mock data
        """
        _api = [
            '/api/v1/platform/user/login',
            '/api/v1/platform/project/list'
        ]
        return _api


if __name__ == '__main__':
    MockHandler(8888)
