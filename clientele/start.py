# _author: Coke
# _date: 2022/11/21 11:03

from clientele import utils, api, globals
from clientele.sockets import socket, create_app
from clientele.actuator import workers

import multiprocessing
import socketio.exceptions
import logging
import time


tokens = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJXaW5kb3dzIiwidXNlcl9pZCI6IjE5ZjVkNzY4NzZkZDE' \
        'xZWRhMDdiNzBjZDBkMzJlYjMxIiwiZXhwIjpudWxsfQ.e4-Za4wLktQMfbrxQcB2cV0vj6pH2BNLNqtQuAFUMxg'


class ReGetSystemUtilities(utils.GetSystemUtilities):

    def reported(self) -> None:
        try:
            socket.emit('system', data=self.get)
        except socketio.exceptions.BadNamespaceError:
            pass


class Starter:
    """ 启动器 """

    def __init__(self, token, logger=False):

        if logger:
            utils.logger(logger)

        self.worker_process = {}  # 执行机进程
        globals.add('freeTask', True)  # 从服务器获取是否有空闲任务
        self.worker_platform = []  # 当前控制机所绑定的工作机平台类型

        self.token = token
        globals.add('token', token)

        # 创建 socket client
        create_app()

        self.devices = api.Devices()
        master = self.devices.get_master_info
        globals.add('master', master)
        worker = self.devices.get_worker_list({'page': 1, 'pageSize': master['maxContext'], 'master': master['id']})
        globals.add('worker', worker.get('items'))

    @property
    def get_master(self):
        """ 获取控制机信息 """
        return globals.get('master')

    @property
    def get_worker(self):
        """ 获取工作机信息 """
        worker = globals.get('worker')
        for item in worker:

            # 如果工作机处于停止状态则不将此信息添加
            if not item.get('switch'):
                continue

            _platform = item['platformName'].upper()
            if _platform not in self.worker_platform:
                self.worker_platform.append(_platform)

        logging.debug(f'当前共有 {len(worker)} 个工作机')

        return worker

    @staticmethod
    def get_task(_platform):
        """ 获取一个任务 """
        try:
            task = api.request('GET', '/task/get', json={'platform': _platform})
        except Exception as e:
            logging.error(e)
        else:
            return task

    def get_free_worker(self, _platform=None):
        """ 获取一个空闲的工作机 """

        _platform = _platform if _platform else []
        for item in self.get_worker:

            # 如果当前设备处于停止状态则跳过本次循环
            if not item.get('switch'):
                continue

            # 如果当前设备存在于差异列表中则跳过本设备
            if item.get('platformName').upper() in _platform:
                continue

            # 如果设备未在进程中并且不属于此平台则返回当前设备
            if not self.worker_process.get(item['id']):
                logging.debug(f'{item.get("name")} 设备处于空闲状态')
                return item

    def get_worker_info(self, _id):
        """ 通过 worker id 获取设备信息 """
        for item in self.get_worker:
            if _id == item.get('id'):
                return item
        return {}

    def run(self, interval=1):
        """ 启动运行程序 """
        while True:

            # 查询是否进入任务轮训, 开关为 False 时跳过本次循环, 无空闲任务时终止轮训
            if not self.get_master['status'] or not globals.get('freeTask'):
                logging.debug(f'当前控制机状态: {self.get_master["status"]}, 是否存在任务: {globals.get("freeTask")}')
                time.sleep(interval)
                continue

            _platform = []
            while True:

                _device = self.get_free_worker(_platform)
                # 如果不存在空闲机器则终止
                if not _device:
                    break

                # 如果无无当前控制机所有的平台时，循环终止
                if len(_platform) >= len(self.worker_platform):
                    logging.info('服务器没有当前控制机所有平台的任务')
                    globals.add('freeTask', False)
                    break

                _task = self.get_task(_device['platformName'])
                _task_info = _task.get('task')
                globals.add('freeTask', _task.get('free'))

                # 如果服务器还有任务但是没有当前设备平台的任务时, 再次进入循环
                if _task.get('free') and not _task_info:
                    logging.debug(f'服务器没有 {_device["platformName"]} 平台的任务')
                    if _device['platformName'] not in _platform:
                        _platform.append(_device['platformName'].upper())
                    continue

                # 如果当前服务器没有任务后终止本次循环
                if not _task.get('free') and not _task_info:
                    logging.debug('服务器当前没有任务')
                    break

                # 如果存在空闲设备并且任务为真时，则启动进程
                if _device and _task_info:
                    logging.info(f'已经将任务分发给 {_device["name"]} 设备')
                    _actuator = multiprocessing.Process(
                        target=workers,
                        args=(_device['name'], _device['id'], self.token)
                    )
                    self.worker_process[_device['id']] = _actuator
                    _actuator.start()
                    break

            self._worker_status()

            time.sleep(interval)

    def _worker_status(self):
        """ 查询当前执行机的进程状态并更新数据 """
        for key, value in self.worker_process.items():
            if value and not value.is_alive():
                worker_info = self.get_worker_info(key)
                logging.info(f'{worker_info.get("name")} 任务已经结束了')
                self.worker_process[key] = False


if __name__ == '__main__':
    # 获取电脑硬件信息
    _system = ReGetSystemUtilities()
    _system.start()
    # 执行任务函数
    obj = Starter(tokens, logger=utils.INFO)
    obj.run()
