# _author: Coke
# _date: 2022/11/18 18:36

import multiprocessing
import time
import random
import os
from clientele import utils
import threading


class Actuator(threading.Thread):
    """
    执行器
    通过此方法执行自动化测试
    """

    def __init__(self, **kwargs: dict):
        """

        :param testId: 任务ID
        :param device: 设备名称
        :param kwargs:
        """
        task_id = kwargs.pop('taskId', None)
        self.device = kwargs.pop('device', None)

        if task_id is None:
            raise KeyError('taskId 不能为空')

        if self.device is None:
            raise KeyError('device 不能为空')

        super(Actuator, self).__init__(**kwargs)

    def run(self):
        """
        执行方法
        :return:
        """
        print(f'start {self.device} test')
        time.sleep(random.randint(1, 10))

        print(f'end {self.device} test')
        # utils.kill(self.pid)


if __name__ == '__main__':
    _device = ['iPhone', 'Android']
    for item in _device:
        obj = Actuator(device=item, taskId=1)
        obj.start()
        # _mult = multiprocessing.Process(target=obj.run)
        # _mult.start()

    # time.sleep(11)
