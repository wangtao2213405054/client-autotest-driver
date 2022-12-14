# _author: Coke
# _date: 2022/11/18 18:36

from clientele import globals, api

import time
import random


def workers(name, worker_id, task_id, token):
    globals.add('token', token)

    run_count = random.randint(10, 50)
    print(f'开始 {name} 测试')

    api.request('POST', '/task/report/start', json={'id': task_id, 'count': run_count})
    device = api.Devices()
    device.update_worker_status(id=worker_id, status=1)

    for item in range(run_count):
        random_status = random.randint(1, 4)
        time.sleep(random.randint(1, 10))
        api.request('POST', '/task/report/new', json={'id': task_id, 'name': f'{name}{item}', 'status': random_status})

    print(f'结束 {name} 测试')

    _random = random.choice([True, False])
    if _random:
        device.update_worker_status(id=worker_id, status=2, cause='这是模拟异常的')
    else:
        device.update_worker_status(id=worker_id, status=0)

    api.request('POST', '/task/report/end', json={'id': task_id, 'status': random.randint(2, 3)})

