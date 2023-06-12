# _author: Coke
# _date: 2022/7/20 12:19

from appium.protocols.webdriver.can_execute_commands import CanExecuteCommands
from selenium.webdriver.remote.webelement import WebElement
from typing import TypeVar, Union, Optional
from appium.webdriver import Remote
from clientele import globals

import logging

T = TypeVar('T', bound=CanExecuteCommands)


class Appium:
    """ appium api 基础封装 """

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
            interval: Union[int, float] = 0.5
    ) -> bool: ...

    def find_elements_location(self, by: str, value: str, index: int = 0, name: str = None) -> tuple[int, int]: ...

    def find_elements_size(self, by: str, value: str, index: int = 0, name: str = None) -> tuple[int, int]: ...

    def case(self, steps: dict, name: str) -> None: ...

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

    def background(self, timer: int) -> T:
        """
        将应用置于后台
        :param timer: 置于后台的时间
        :return:
        """

        logging.info(f'将程序置于后台 {timer} 秒')

        return self.driver.background_app(timer)

    def set_location(self, latitude: Union[float, str], longitude: Union[float, str], altitude: Union[float, str]) -> T:
        """
        设置当前设备处于的位置
        :param latitude: 纬度
        :param longitude: 经度
        :param altitude: 高度
        :return:
        """

        logging.info(f'将当前设备位置修改为: 维度{latitude}, 经度{longitude}, 高度{altitude}')

        return self.driver.set_location(latitude, longitude, altitude)

    def uninstall(self, bundle_id: str) -> T:
        """
        卸载当前应用程序
        :param bundle_id: 安装包id, ios: bundleId android: clientele package
        :return:
        """

        if self.driver.is_app_installed(bundle_id):
            logging.info('正在卸载当前应用程序')

            return self.driver.remove_app(bundle_id)

    def get_android_bundle(self) -> tuple[str, str]:
        """
        获取当前 Android 设备运行包的 clientele package and clientele activity
        :return:
        """

        package = self.driver.current_package
        activity = self.driver.current_activity

        logging.info(f'当前运行应用信息: package: {package}, activity: {activity}')

        return package, activity

    @staticmethod
    def _swipe(width: Union[int, float], height: Union[int, float], start: float, end: float) -> dict:
        swipe = dict(
            vertical=dict(desc='纵向滑动', value=[0.5 * width, start * height, 0.5 * width, end * height]),
            horizontal=dict(desc='横向滑动', value=[start * width, 0.5 * height, end * width, 0.5 * height])
        )
        return swipe

    def find_window_swipe(self, handle: str, start: float, end: float, duration: Union[int, float]) -> Optional[T]:
        """
        在当前设备上滑动
        开始位置和结束位置分别需要一个百分比小数
        按比例进行滑动, 设备 宽/高 * 开始/结束 比率
        宽高从设备的左上角开始计算
        :param handle: 滑动方向
        :param start: 开始位置比例
        :param end: 结束位置比例
        :param duration: 滑动时长 s
        :return:
        """

        duration *= 1000
        width, height = self.get_window_size()

        swipe = self._swipe(width, height, start, end)

        direction = swipe.get(handle)
        if not direction:
            logging.info(f'{handle} 此句柄方向不存在')
            return None

        logging.info(f'在手机屏幕上 {direction.get("desc")}')

        return self.driver.swipe(*direction.get('value'), int(duration))

    def quit(self):
        """ 关闭应用 """
        self.driver.terminate_app(globals.get('appId'))
