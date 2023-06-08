# _author: Coke
# _date: 2022/8/1 10:18

from clientele import drivers, api, utils
from typing import Any

import logging
import time


class CaseEvent(drivers.Driver):
    """
    测试用例事件统一入口
    方便 getattr 调用
    """

    def __init__(self, driver, wait=5):
        self.imagePaths = []
        self.images = []
        super().__init__(driver, wait)

    @staticmethod
    def show_wait(timer) -> None:
        """
        显示等待
        :param timer: 要等待的时间 s
        :return:
        """
        logging.info(f'等待 {timer} 秒')
        time.sleep(timer)

    def attribute(self, **kwargs) -> None: ...

    def url_screenshots(self) -> str:
        """ 继承 screenshots 方法后将图片上传至云端并返回 url 链接 """
        path = self.screenshots()
        url = api.upload_file(path).get('url')
        if url:
            self.images.append(url)
        return url

    def save_screenshots(self, file_path: str = None, is_compression: bool = False) -> str:
        """
        重写 screenshots 方法, 并将图片地址存放在 imagePaths 中
        :param file_path:
        :param is_compression:
        :return:
        """
        path = self.screenshots(file_path, is_compression)
        self.imagePaths.append(path)
        return path

    @staticmethod
    def update_globals_variable(key: str, value: Any, types: str) -> None:
        """
        新增/修改内存变量信息
        :param key: 变量名称
        :param value: 存储的值
        :param types: 存储值的数据类型
        :return:
        """
        utils.add(key, utils.transition(value, types))

    @staticmethod
    def assert_globals_variable(key: str, condition: str, value: Any, types: str) -> bool:
        """
        断言内存变量是否符合条件
        :param key: 内存变量中的Key
        :param condition: 要断言的条件
        :param value: 要断言的值
        :param types: 要断言值的类型
        :return:
        """

        return utils.operation(utils.get(key), condition, utils.transition(value, types))

    @staticmethod
    def raise_error():
        raise PermissionError('这是一个测试的步骤')
