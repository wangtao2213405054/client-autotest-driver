import time

from clientele import api

import threading

_list = []


def test():
    while True:
        data = api.request('GET', '/task/get')
        if data:
            _list.append(data.get('taskId'))


if __name__ == '__main__':
    for item in range(8):
        obj = threading.Thread(target=test, daemon=True)
        obj.start()
    time.sleep(10)
    print(_list)
