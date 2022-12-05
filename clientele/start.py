# _author: Coke
# _date: 2022/11/21 11:03

from clientele import sio, utils, create_app, Actuator, api
import socketio.exceptions

import time


token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJNYWMiLCJ1c2VyX2lkIjoiZTMxMTA5YWE2ZWZhMTFlZDhhY' \
        'jQ3MGNkMGQzMmViMzEiLCJleHAiOm51bGx9.wYm_yHVYBEMbqnCaWg_RJg38ltjqgQbZUKDA8x_z1To'

# 这是假设从服务器获取的设备信息
_devices = [
    {'id': 1, 'name': 'iPhone'},
    {'id': 2, 'name': 'Android'}
]

# 进程存储器
_process = {}

# 创建 socket 服务
create_app(token)


class ReGetSystemUtilities(utils.GetSystemUtilities):

    def reported(self) -> None:
        try:
            print(self.get)
            sio.emit('system', data=self.get)
        except socketio.exceptions.BadNamespaceError:
            pass


_system = ReGetSystemUtilities()
_system.start()


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
    main()
