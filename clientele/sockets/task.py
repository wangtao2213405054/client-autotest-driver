# _author: Coke
# _date: 2022/11/18 15:23

from clientele.sockets import socket
from clientele import globals

import logging


@socket.on('taskFree')
def update_master_free():
    """ 通知控制机有新的任务 """

    globals.add('freeTask', True)
    logging.info('更新控制机任务为 True')
