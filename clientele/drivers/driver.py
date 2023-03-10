# _author: Coke
# _date: 2022/7/20 12:02

from selenium.webdriver import Remote
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import NoSuchElementException
from clientele import utils, drivers
from typing import Union

import logging
import time
import os


class Driver(drivers.Selenium, drivers.Appium):
    """ 基于 selenium 和 appium 通用模块的封装, 如果为独有方法则封装在对象的 class 中 """

    def __init__(self, driver: Remote, element_wait: Union[int, float] = 5):
        """
        初始化类, 对于 基础操作的二次封装, 继承于 Selenium 和 Appium 类
        :param driver: selenium or appium 的驱动类
        :param element_wait: 等待元素出现的时间
        """
        super().__init__(driver)

        try:
            driver.implicitly_wait(element_wait)
        except AttributeError:
            pass
        self.driver = driver

    def find_elements(self, by: str, value: str, name: str = None) -> list[WebElement]:
        """
        查询元素, 返回 list
        :param by: 元素类型
        :param value: 元素值
        :param name: 元素名称
        :return:
        """

        elements = self.driver.find_elements(by, value)

        logging.debug(f'共找到 {len(elements)} 个 {name}')

        return elements

    def find_elements_click(self, by: str, value: str, index: int = 0, name: str = None) -> None:
        """
        点击操作
        :param by: 元素类型
        :param value: 元素值
        :param index: 索引
        :param name: 元素名称
        :return:
        """

        logging.info(f'准备点击第 {index + 1} 个 {name or value}')

        elements = self.find_elements(by, value, name=name)
        if len(elements) < index + 1:
            raise NoSuchElementException(f'没有找到 {name or value} 元素')

        return elements[index].click()

    def find_elements_clear(self, by: str, value: str, index: int = 0, name: str = None) -> None:
        """
        清空文本输入框
        :param by: 元素类型
        :param value: 元素值
        :param index: 索引
        :param name: 元素名称
        :return:
        """

        logging.info(f'准备清空第 {index + 1} 个 {name} 的值')

        elements = self.find_elements(by, value, name=name)
        if len(elements) < index + 1:
            raise NoSuchElementException(f'没有找到 {name or value} 元素')

        return elements[index].clear()

    def find_elements_send_keys(self, by: str, value: str, content: str, index: int = 0, name: str = None) -> None:
        """
        在文本框中进行输入
        :param by: 元素类型
        :param value: 元素值
        :param content: 输入的内容
        :param index: 索引
        :param name: 元素名称
        :return:
        """

        logging.info(f'准备在第 {index + 1} 个 {name} 中输入: "{content}"')

        elements = self.find_elements(by, value, name=name)
        if len(elements) < index + 1:
            raise NoSuchElementException(f'没有找到 {name or value} 元素')

        return elements[index].send_keys(content)

    def find_elements_location(self, by: str, value: str, index: int = 0, name: str = None) -> tuple[int, int]:
        """
        获取当前元素所处的坐标
        :param by: 元素类型
        :param value: 元素值
        :param index: 索引
        :param name: 元素名称
        :return:
        """

        elements = self.find_elements(by, value, name=name)
        if len(elements) < index + 1:
            raise NoSuchElementException(f'没有找到 {name or value} 元素')

        x = elements[index].location.get('x')
        y = elements[index].location.get('y')
        logging.info(f'第 {index + 1} 个 {name or value} 所处的坐标为: x: {x}, y: {y}')

        return x, y

    def find_elements_size(self, by: str, value: str, index: int = 0, name: str = None) -> tuple[int, int]:
        """
        查找当前元素所在大小
        :param by: 元素类型
        :param value: 元素值
        :param index: 索引
        :param name: 元素名称
        :return:
        """

        elements = self.find_elements(by, value, name=name)
        if len(elements) < index + 1:
            raise NoSuchElementException(f'没有找到 {name or value} 元素')

        width = elements[index].size.get('width')
        height = elements[index].size.get('height')

        logging.info(f'第 {index + 1} 个 {name or value} 元素大小: 宽{width}, 高{height}')

        return width, height

    def get_window_size(self) -> tuple[int, int]:
        """
        获取窗口宽高
        :return:
        """
        width = self.driver.get_window_size().get('width')
        height = self.driver.get_window_size().get('height')

        logging.info(f'当前设备窗口大小: 宽度{width}, 高度{height}')

        return width, height

    def wait_elements_appear(
            self,
            by: str,
            value: str,
            index: int = 0,
            name: str = None,
            wait_time: Union[float, int] = 5,
            interval: Union[float, int] = 0.5
    ) -> bool:
        """
        等待元素出现
        :param by: 元素类型
        :param value: 元素值
        :param index: 索引
        :param name: 元素名称
        :param wait_time: 最大等待时间
        :param interval: 检测间隔
        :return:
        """

        end_time = time.monotonic() + wait_time

        while True:
            current_time = time.monotonic()
            if current_time > end_time:
                break

            elements = self.find_elements(by, value, name)
            if len(elements) >= index + 1:
                logging.info(f'在 {end_time - current_time} 秒内找到了 {name or value} 元素')
                return True

            time.sleep(interval)
        logging.info(f'在 {float(wait_time)} 秒内没有找到 {name or value} 元素')
        return False

    def screenshots(self, file_path: str = None, is_compression: bool = True) -> str:
        """
        对设备当前屏幕进行截图
        :param file_path: 截图存储路径
        :param is_compression: 是否对图片进行压缩
        :return:
        """
        if not file_path:
            folder_path = utils.set_path('screenshots')
            file_path = os.path.join(folder_path, f"{int(time.time() * 1000)}.png")

        self.driver.get_screenshot_as_file(file_path)

        if is_compression:
            utils.measure(file_path, 0.7)
            utils.compress(file_path, 800)

        return file_path

    def find_elements_screenshots(
            self,
            by: str,
            value: str,
            index: int = 0,
            name: str = None,
            file_path: str = None,
            is_compression: bool = False
    ) -> str:
        """
        根据元素进行截图
        :param by: 元素类型
        :param value: 元素值
        :param index: 索引
        :param name: 元素名称
        :param file_path: 文件保存路径
        :param is_compression: 是否压缩
        :return: 返回图片地址
        """

        # 截图并获取元素所在区域
        screenshot = self.screenshots(file_path, is_compression)
        start_x, start_y = self.find_elements_location(by, value, index, name)
        width, height = self.find_elements_size(by, value, index, name)
        end_x = start_x + width
        end_y = start_y + height

        # 计算 图片宽高 和 设备宽高的比率
        image = utils.Image.open(screenshot)
        image_width, image_height = image.size
        window_width, window_height = self.get_window_size()
        multiple = (int(image_width / window_width) + int(image_height / window_height)) / 2

        area = tuple(map(lambda x: int(x * multiple), (start_x, start_y, end_x, end_y)))
        aspect = (width, height)

        return utils.cut(screenshot, area, aspect)
