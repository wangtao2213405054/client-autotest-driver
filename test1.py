# _author: Coke
# _date: 2022/7/26 21:32

import threading
import os
import time
import socket
import utils
import sys


def create_server():
    """ 启动一个 appium server """

    os.popen('appium')


if __name__ == '__main__':
    thread = threading.Thread(target=create_server, daemon=True)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = s.connect_ex(('0.0.0.0', 4723))
    print(result)
    thread.start()
    time.sleep(3)
    utils.kill_prot(4723)
