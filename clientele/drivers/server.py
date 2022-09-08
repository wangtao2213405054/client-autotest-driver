# _author: Coke
# _date: 2022/7/29 10:29

import threading
import platform
import logging
import os


class DriversServer:
    """
    启动 appium 所需要的 server
    如 appium 服务器
    iOS 所依赖的 web driver agent 服务
    """

    def __init__(self, **kwargs):
        """
        实例化类
        :param kwargs: 设备的配置文件信息
        """
        self.platform = kwargs.get('platform')
        self.conf = kwargs

        if self.platform.upper() == 'iOS'.upper() and platform.system() == 'Windows':
            _message = 'Windows 不支持 iOS 设备'
            logging.critical(_message)
            raise SystemError(_message)

    def start_appium(self) -> None:
        """
        启动 appium 服务器
        """
        _port = self.conf.get('appiumPort')
        _order = f'appium -a 127.0.0.1 -p {_port} --session-override'

        if platform.system() == 'Darwin':
            _agent_port = self.conf.get('webdriverPort')
            _order += f' --webdriveragent-port {_agent_port}'

        os.popen(_order)

    def start_webdriver(self) -> None:
        """
        启动 webDriver agent 服务器
        由于本机没有安装 xcode ...
        等安装后查看 xcodebuild 具体的运行方式
        """
        _webdriver_path = ''
        _udid = self.conf.get('udid')
        _order = f'xcodebuild -project {_webdriver_path} -scheme WebDriverAgentRunner -destination "id={_udid}" test'

        os.popen(_order)

    def run(self) -> None:
        """
        启动 appium 相关的服务
        """
        _appium_thread = threading.Thread(target=self.start_appium)
        _appium_thread.start()

        if platform.system() == 'Darwin':
            _webdriver_thread = threading.Thread(target=self.start_webdriver)
            _webdriver_thread.start()
