# _author: Coke
# _date: 2022/7/20 12:19

from selenium.webdriver.remote.webelement import WebElement
from appium.webdriver import Remote
from appium.webdriver.common.touch_action import TouchAction

import logging


class Appium:
    """ appium api 基础封装 """

    def __init__(self, driver: Remote):
        self.driver = driver

    def find_elements(self, by, value) -> list[WebElement]: ...

    def find_elements_click(self, by, value, index=0, name=None) -> None: ...

    def find_elements_clear(self, by, value, index=0, name=None) -> None: ...

    def find_elements_send_keys(self, by, value, content, index=0, name=None) -> None: ...

    def get_window_size(self) -> tuple[int, int]: ...

    def wait_elements_appear(self, by, value, index=0, name=None, wait_time=5, interval=0.5) -> tuple[bool, str]: ...

    def find_elements_location(self, by, value, index=0, name=None) -> tuple[int, int]: ...

    def find_elements_size(self, by, value, index=0, name=None) -> tuple[int, int]: ...

    def screenshots(self, file_path=None, is_compression=True) -> str: ...

    def find_elements_screenshots(self, by, value, index=0, name=None, file_path=None, is_compression=False) -> str: ...

    def background(self, timer):
        """
        将应用置于后台
        :param timer: 置于后台的时间
        :return:
        """

        logging.info(f'将程序置于后台 {timer} 秒')

        return self.driver.background_app(timer)

    def set_location(self, latitude, longitude, altitude):
        """
        设置当前设备处于的位置
        :param latitude: 纬度
        :param longitude: 经度
        :param altitude: 高度
        :return:
        """

        logging.info(f'将当前设备位置修改为: 维度{latitude}, 经度{longitude}, 高度{altitude}')

        return self.driver.set_location(latitude, longitude, altitude)

    def uninstall(self, bundle_id):
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
    def _swipe(width, height, start: float, end: float) -> dict:
        swipe = dict(
            vertical=dict(desc='纵向滑动', value=[0.5 * width, start * height, 0.5 * width, end * height]),
            horizontal=dict(desc='横向滑动', value=[start * width, 0.5 * height, end * width, 0.5 * height])
        )
        return swipe

    def find_window_swipe(self, handle, start: float, end: float, duration=0.5):
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

    def find_element_swipe(self, by, value, index=0, name=None, handle='vertical', start=0.8, end=0.2, duration=0.5):
        """
        寻找到指定的元素后在元素中进行按压滑动
        :param by: 元素类型
        :param value: 元素值
        :param index: 索引
        :param name: 元素名称
        :param handle: 滑动方向
        :param start: 开始位置比例
        :param end: 结束位置比例
        :param duration: 滑动时间
        :return:
        """
        duration *= 1000
        start_x, start_y = self.find_elements_location(by, value, index, name)
        width, height = self.find_elements_size(by, value, index, name)
        width += start_x
        height += start_y

        swipe = self._swipe(width, height, start, end)
        axis = swipe.get(handle)

        action = TouchAction(self.driver)
        return action.press(*axis[0: 2]).wait(int(duration)).move_to(*axis[2: 4]).release().perform()
