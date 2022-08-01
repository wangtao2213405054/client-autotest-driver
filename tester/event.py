# _author: Coke
# _date: 2022/8/1 10:18

import drivers
import logging
import time


class CaseEvent(drivers.Driver):
    """
    测试用例事件统一入口
    方便 getattr 调用
    """

    def __init__(self, driver, wait):
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
