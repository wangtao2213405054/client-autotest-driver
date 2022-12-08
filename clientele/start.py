# _author: Coke
# _date: 2022/11/21 11:03

from clientele import utils, Actuator, api
from clientele.sockets import socket, create_app

import socketio.exceptions
import time


token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJXaW5kb3dzIiwidXNlcl9pZCI6IjE5ZjVkNzY4NzZkZDE' \
        'xZWRhMDdiNzBjZDBkMzJlYjMxIiwiZXhwIjpudWxsfQ.e4-Za4wLktQMfbrxQcB2cV0vj6pH2BNLNqtQuAFUMxg'

# 这是假设从服务器获取的设备信息
_devices = [
    {'id': 1, 'name': 'iPhone'},
    {'id': 2, 'name': 'Android'}
]

# 进程存储器
_process = {}


class ReGetSystemUtilities(utils.GetSystemUtilities):

    def reported(self) -> None:
        try:
            socket.emit('system', data=self.get)
        except socketio.exceptions.BadNamespaceError:
            pass


def main():
    """
    运行函数
    :return:
    """
    while True:

        # 获取任务
        for device in _devices:
            if not _process.get(device['id']):
                _data = api.request('GET', '/task/get')
                if _data:
                    _task = Actuator(device=_data.get('taskName'), taskId=_data.get('taskId'), daemon=True)
                    _task.start()
                    _process[device['id']] = _task
                else:
                    time.sleep(1)
                    break

        time.sleep(0.5)

        # 检查自动化任务进程
        for device, task in _process.items():
            if task and not task.is_alive():
                _process[device] = False


if __name__ == '__main__':
    # 创建 socket 服务
    create_app(token)
    # 获取电脑硬件信息
    _system = ReGetSystemUtilities()
    _system.start()
    # 执行任务函数
    main()
