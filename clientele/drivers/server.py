# _author: Coke
# _date: 2022/7/29 10:29

import multiprocessing
import platform
import logging
import os


class AppiumProcess(multiprocessing.Process):
    """
    启动 appium 服务器
    """

    def __init__(self, appium_port, webdriver_port, **kwargs):

        self.appium_port = appium_port
        self.webdriver_port = webdriver_port

        super(AppiumProcess, self).__init__(**kwargs)

    def run(self) -> None:
        _order = f'appium -a 127.0.0.1 -p {self.appium_port} --session-override'

        if platform.system() == 'Darwin':
            _order += f' --webdriveragent-port {self.webdriver_port}'

        logging.debug(f'启动 appium 服务器, 端口: {self.appium_port}')
        logging.debug(f'启动命令: {_order}')
        os.system(_order)


class WebdriverProcess(multiprocessing.Process):
    """
    启动 webdriver agent 服务器
    """

    def __init__(self, path, udid, **kwargs):
        self.path = path
        self.udid = udid
        super(WebdriverProcess, self).__init__(**kwargs)

    def run(self) -> None:
        _order = f'xcodebuild -project {self.path} -scheme WebDriverAgentRunner -destination "id={self.udid}" test'

        logging.debug(f'启动 WebDriverAgent 服务, 指定设备udid: {self.udid}')
        logging.debug(f'启动命令: {_order}')
        os.system(_order)
