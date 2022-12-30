# _author: Coke
# _date: 2022/8/1 10:18

from clientele import drivers
import logging
import time


class CaseEvent(drivers.Driver):
    """
    测试用例事件统一入口
    方便 getattr 调用
    """

    def __init__(self, driver, wait=5):
        self.imagePaths = []
        super().__init__(driver, wait)

    @staticmethod
    def show_wait(timer):
        """
        显示等待
        :param timer: 要等待的时间 s
        :return:
        """
        logging.info(f'等待 {timer} 秒')
        time.sleep(timer)

    def attribute(self, **kwargs): ...

    def screenshots(self, file_path: str = None, is_compression: bool = True) -> str:
        """
        重写 screenshots 方法
        :param file_path:
        :param is_compression:
        :return:
        """
        try:
            path = super().screenshots(file_path, is_compression)
            self.imagePaths.append(path)
            return path
        except Exception as e:
            logging.debug(e)
