# _author: Coke
# _date: 2022/11/21 11:03

from clientele import utils, api, globals
from clientele.sockets import socket, create_app
from clientele.actuator import workers

import multiprocessing
import socketio.exceptions
import logging
import time


tokens = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJXaW5vZHdzIiwidXNlcl9pZCI6ImVjYzM5ODhkN2I3N' \
         'TExZWRhMTA4NzBjZDBkMzJlYjMxIiwiZXhwIjpudWxsfQ.tyLzZFQXHHDzIWESIeztnYMTiSPHDnF9JhnVt-MKmqI'


class ReGetSystemUtilities(utils.GetSystemUtilities):

    def reported(self) -> None:
        try:
            socket.emit('system', data=self.get)
        except socketio.exceptions.BadNamespaceError:
            pass


# 执行机进程对象
worker_process = {}


class Starter:
    """ 启动器 """

    def __init__(self, token, logger=False):

        if logger:
            utils.logger(logger)

        globals.add('freeTask', True)  # 从服务器获取是否有空闲任务

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
        return globals.get('worker')

    @staticmethod
    def get_task(body):
        """ 获取一个任务 """
        return api.request('GET', '/task/master/get', json=body, exceptions=Exception)

    @staticmethod
    def recall(_id):
        """ 回溯任务状态 """
        return api.request('POST', '/task/master/sign', json={'id': _id}, exceptions=Exception)

    @property
    def get_free_worker(self):
        """ 获取空闲的工作机列表 """
        worker = globals.get('worker')
        _worker_list = []
        for item in worker:
            if not worker_process.get(item['id']) and item.get('switch'):
                _worker_list.append(item)

        logging.info(f'当前共有 {len(_worker_list)} 个空闲的工作机')
        return _worker_list

    def get_worker_info(self, _id):
        """ 通过 worker id 获取设备信息 """
        for item in self.get_worker:
            if _id == item.get('id'):
                return item
        return {}

    def run(self, interval=1):
        """ 启动运行程序 """

        while True:

            time.sleep(interval)

            self._worker_status()

            # 查询是否进入任务轮训, 开关为 False 时跳过本次循环, 无空闲任务时终止轮训
            if not self.get_master['status'] or not globals.get('freeTask'):
                logging.debug(f'当前控制机状态: {self.get_master["status"]}, 是否存在任务: {globals.get("freeTask")}')
                continue

            # 查询空闲设备
            free_worker = list(map(lambda x: x.get('id'), self.get_free_worker))
            if not free_worker:
                continue

            _task = self.get_task({'free': free_worker})

            if not _task:
                logging.error('任务获取失败, 请检查失败原因')
                continue

            globals.add('freeTask', _task.get('free'))
            _task_list = _task.get('task')

            for _task_item in _task_list:
                _id = _task_item.get('power')
                _device = self.get_worker_info(_id)
                # 如果id在空闲设备列表并且此设备开关状态正常、进程正常，然后将任务分发
                if _id in free_worker and _device.get('switch') and not worker_process.get(_id):
                    logging.info(f'已经将任务分发给 {_device.get("name")} 设备')
                    _actuator = multiprocessing.Process(
                        target=workers,
                        args=(_device.get("name"), _id, _task_item.get('id'), self.token)
                    )
                    worker_process[_id] = _actuator
                    _actuator.start()
                else:
                    # 通知服务器, 此任务未分配，数据回滚
                    self.recall(_task_item.get('id'))

    def _worker_status(self):
        """ 查询当前执行机的进程状态并更新数据 """
        for key, value in worker_process.items():
            if value and not value.is_alive():
                worker_info = self.get_worker_info(key)
                logging.info(f'{worker_info.get("name")} 任务已经结束了')
                worker_process[key] = False


if __name__ == '__main__':
    # 获取电脑硬件信息
    _system = ReGetSystemUtilities()
    _system.start()
    # 执行任务函数
    obj = Starter(tokens, logger=utils.INFO)
    obj.run()
