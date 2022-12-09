# _author: Coke
# _date: 2022/12/9 10:57

from clientele import api
from clientele import globals

import requests.exceptions


class Devices:
    """ 设备相关API """

    @property
    def get_master_info(self):
        """ 获取当前设备的信息 """

        return api.request('GET', '/devices/master/info', exceptions=(requests.exceptions.ConnectionError, ))

    @staticmethod
    def get_worker_list(data):
        """ 获取当前设备绑定的执行机 """

        return api.request('GET', '/devices/worker/list', json=data, exceptions=(requests.exceptions.ConnectionError, ))

    @staticmethod
    def update_worker_status(**kwargs):
        """ 修改工作机状态 """
        return api.request('POST', '/devices/worker/status', json=kwargs)


if __name__ == '__main__':
    obj = Devices()
    globals.add('token', 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX25hbWUiOiJXaW5kb3d'
                         'zIiwidXNlcl9pZCI6IjE5ZjVkNzY4NzZkZDE'
        'xZWRhMDdiNzBjZDBkMzJlYjMxIiwiZXhwIjpudWxsfQ.e4-Za4wLktQMfbrxQcB2cV0vj6pH2BNLNqtQuAFUMxg')
    master = obj.get_master_info
    print(master)
    print(obj.get_worker_list({'page': 1, 'pageSize': master['maxContext'], 'master': master['id']}))
