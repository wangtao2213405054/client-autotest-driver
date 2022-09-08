# _author: Coke
# _date: 2022/7/20 12:19

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver import Remote
from clientele import utils
from typing import Union

import logging
import json


class Selenium:
    """ selenium api 基础封装 """

    def __init__(self, driver: Remote):
        self.driver = driver

    def find_elements(self, by: str, value: str) -> list[WebElement]: ...

    def find_elements_click(self, by: str, value: str, index: int = 0, name: str = None) -> None: ...

    def find_elements_clear(self, by: str, value: str, index: int = 0, name: str = None) -> None: ...

    def find_elements_send_keys(self, by: str, value: str, content: str, index: int = 0, name: str = None) -> None: ...

    def get_window_size(self) -> tuple[int, int]: ...

    def wait_elements_appear(
            self,
            by: str,
            value: str,
            index: int = 0,
            name: str = None,
            wait_time: Union[int, float] = 5,
            interval: Union[float, int] = 0.5
    ) -> tuple[bool, str]: ...

    def find_elements_location(self, by: str, value: str, index: int = 0, name: str = None) -> tuple[int, int]: ...

    def find_elements_size(self, by: str, value: str, index: int = 0, name: str = None) -> tuple[int, int]: ...

    def screenshots(self, file_path: str = None, is_compression: bool = True) -> str: ...

    def find_elements_screenshots(
            self,
            by: str,
            value: str,
            index: int = 0,
            name: str = None,
            file_path: str = None,
            is_compression: bool = False
    ) -> str: ...

    def quit(self) -> None:
        """
        关闭当前浏览器
        """
        logging.info('关闭浏览器进程')
        self.driver.quit()

    def close(self) -> None:
        """
        关闭当前浏览器页面
        """
        logging.info('关闭当前浏览页面')
        self.driver.close()

    def save_cookies(self) -> None:
        """
        获取当前浏览器的 cookies 并存储在本地变量中
        """
        logging.info('正在获取当前页面的Cookies并存储')
        cookies = self.driver.get_cookies()
        utils.add('cookies', json.dumps(cookies))
        utils.add('loginStatus', True)

    def write_cookies(self) -> None:
        """
        将 cookies 写入浏览器
        """
        logging.info('正在将已存储的Cookies写入浏览器')
        for cookie in json.loads(utils.get('cookies')):
            self.driver.add_cookie(cookie)

    def delete_cookies(self) -> None:
        """
        将浏览器中的 Cookies 删除
        """
        logging.info('正在将浏览器中的Cookies删除')
        self.driver.delete_all_cookies()

    def refresh(self) -> None:
        """
        刷新当前浏览器
        """
        logging.info('正在刷新当前页面')
        self.driver.refresh()

    def back(self) -> None:
        """
        返回到上一级页面
        """

        logging.info('正在返回到上一级页面')
        self.driver.back()

    def selenium_forward_browser(self) -> None:
        """
        前进到下一级页面
        """

        logging.info('正在前进到下一级页面')
        self.driver.forward()

    def switch_window(self, window: int) -> None:
        """
        切换窗口, 需要一个窗口位置
        """

        logging.info(f'正在切换窗口, 切换至{"最新" if window == -1 else f"第 {window + 1} 个"}窗口')
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[window])

    def context_click(self, by: str, value: str, index: int, name: str) -> None:
        """
        selenium 右击事件
        :param by: 元素属性
        :param value: 元素内容
        :param index: 元素索引
        :param name: 元素名称
        :return:
        """
        logging.info(f'右击第 {index + 1} 个 {name}')
        element = self.find_elements(by, value)[index]
        ActionChains(self.driver).context_click(element).perform()

    def double_click(self, by: str, value: str, index: int, name: str) -> None:
        """
        selenium 双击事件
        :param by: 元素属性
        :param value: 元素内容
        :param index: 元素索引
        :param name: 元素名称
        :return:
        """
        logging.info(f'双击第 {index + 1} 个 {name}')
        element = self.find_elements(by, value)[index]
        ActionChains(self.driver).double_click(element).perform()

    def move_element(self, by: str, value: str, index: int, name: str) -> None:
        """
        selenium 鼠标悬停事件
        :param by: 元素属性
        :param value: 元素内容
        :param index: 元素索引
        :param name: 元素名称
        :return:
        """
        logging.info(f'鼠标悬停到第 {index + 1} 个 {name}')
        element = self.find_elements(by, value)[index]
        ActionChains(self.driver).move_to_element(element).perform()
