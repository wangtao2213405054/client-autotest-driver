# _author: Coke
# _date: 2022/7/26 18:28

from clientele import utils, mock, api, globals

import logging


class MockHandler:
    """
    mock 服务主入口
    依赖于 mitmproxy
    """

    def __init__(self, port: int, project_id: int):
        """
        初始化 Mock 相关信息及配置
        :param port: 要启动的端口号
        :param project_id: 项目 ID
        """
        self._port = port
        self._domain = list(map(lambda x: x.get('domain'), api.get_mock_domain_list(project_id)))
        self._api = api.get_mock_api_list(project_id)
        _mock = mock.CreateMockCode(self._api)
        self._code_file = _mock.create_file()
        _mock.create_api_info()

    def start_server(self):
        """
        线程启动 mitmproxy 服务器
        :return:
        """
        _result = utils.usage_port('127.0.0.1', self._port)
        if _result:
            logging.warning(f'端口: {self._port} 已被占用, 准备 kill 掉')
            utils.kill_port(self._port)

        process = mock.MitmproxyProcess(
            self._code_file,
            self._port,
            self._domain,
            daemon=True
        )
        process.start()


if __name__ == '__main__':
    globals.add('token', '')
    obj = MockHandler(8080, 2)
    obj.start_server()
    import time
    time.sleep(1000)
