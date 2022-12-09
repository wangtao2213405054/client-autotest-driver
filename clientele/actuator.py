# _author: Coke
# _date: 2022/11/18 18:36

from clientele import globals, api

import time
import random


def workers(name, worker_id, token):
    globals.add('token', token)

    print(f'开始 {name} 测试')
    device = api.Devices()
    device.update_worker_status(id=worker_id, status=1)
    time.sleep(random.randint(1, 10))

    print(f'结束 {name} 测试')
    _random = random.choice([True, False])
    if _random:
        device.update_worker_status(id=worker_id, status=2, cause='这是模拟异常的')
    else:
        device.update_worker_status(id=worker_id, status=0)


if __name__ == '__main__':
    _device = ['iPhone', 'Android']
    for item in _device:
        pass
