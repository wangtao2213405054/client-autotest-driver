# _author: Coke
# _date: 2022/11/18 18:36

from clientele import globals, api

import time
import random


def workers(name, worker_id, task_id, token, kwargs):
    globals.add('token', token)

    run_count = len(kwargs.get('cases'))
    print(f'开始 {name} 测试')

    api.request('POST', '/task/center/status', json={'id': task_id, 'status': 1, 'device': worker_id})
    api.update_worker_status(dict(id=worker_id, status=1))

    for item in range(run_count):
        random_status = random.randint(1, 4)
        time.sleep(random.randint(1, 10))
        api.request('POST', '/task/report/new', json={'id': task_id, 'name': f'{name}{item}', 'status': random_status})

    print(f'结束 {name} 测试')

    _random = random.choice([True, False])
    if _random:
        api.update_worker_status(dict(id=worker_id, status=1, cause='这是模拟异常的'))
    else:
        api.update_worker_status(dict(id=worker_id, status=0))

    api.request(
        'POST',
        '/task/center/status',
        json={'id': task_id, 'status': random.randint(2, 3), 'device': worker_id}
    )
