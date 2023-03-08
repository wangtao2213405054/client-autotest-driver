# _author: Coke
# _date: 2022/12/9 10:57

from clientele import api

import requests.exceptions


def get_master_info() -> api.request:
    """ 获取当前设备的信息 """

    return api.request(
        'GET',
        '/devices/master/info',
        exceptions=(requests.exceptions.ConnectionError, )
    )


def get_worker_list(body: dict) -> api.request:
    """ 获取当前设备绑定的执行机 """

    return api.request(
        'GET',
        '/devices/worker/list',
        json=body,
        exceptions=(requests.exceptions.ConnectionError,)
    )


def update_worker_status(body: dict) -> api.request:
    """ 修改工作机状态 """

    return api.request(
        'POST',
        '/devices/worker/status',
        json=body
    )
