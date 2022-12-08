# _author: Coke
# _date: 2022/12/8 14:59

from clientele.sockets import socket
from clientele import utils

import os


@socket.on('workerTaskSwitch')
def edit_worker_switch(data):
    """ 获取任务机可执行状态 """
    print(data, 'workerTaskSwitch')


@socket.on('masterTaskSwitch')
def edit_master_switch(data):
    """ 获取当前控制机的执行状态 """
    print(data, 'masterTaskSwitch')


@socket.on('masterDeviceDelete')
def delete_master_info():
    """ 控制设备被删除时调用 """
    socket.sleep(1)
    pid = os.getpid()
    utils.kill(pid)


@socket.on('workerDeviceDelete')
def delete_worker_info(data):
    """ 执行设备被删除时的钩子 """

    print(data, 'workerDeviceDelete')


@socket.on('masterDeviceEdit')
def edit_master_info(data):
    """ 控制设备信息更新时调用 """

    print(data, 'masterDeviceEdit')


@socket.on('workerDeviceEdit')
def edit_worker_info(data):
    """ 执行设备信息更新时调用 """

    print(data, 'workerDeviceEdit')
