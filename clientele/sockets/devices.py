# _author: Coke
# _date: 2022/12/8 14:59

from clientele.sockets import socket
from clientele import utils, globals

import logging
import os


@socket.on('workerTaskSwitch')
def edit_worker_switch(data):
    """ 修改任务机可执行状态 """

    worker = globals.get('worker')
    switch = data.get('switch')
    for item in worker:
        if item.get('id') == data.get('workerId'):
            item['switch'] = switch

    globals.add('worker', worker)
    globals.add('freeTask', True)
    logging.info(f'执行机器{"开启" if switch else "关闭"}任务轮训')


@socket.on('masterTaskSwitch')
def edit_master_switch(data):
    """ 获取当前控制机的执行状态 """

    master = globals.get('master')
    switch = data.get("switch")
    master['status'] = switch
    globals.add('master', master)
    globals.add('freeTask', True)
    logging.info(f'控制机器{"开启" if switch else "关闭"}任务轮训')


@socket.on('masterDeviceDelete')
def delete_master_info():
    """ 控制设备被删除时调用 """
    _time = 1
    logging.info(f'此驱动端 {_time} 秒后将停止进程')
    socket.sleep(_time)
    pid = os.getpid()
    utils.kill(pid)


@socket.on('workerDeviceDelete')
def delete_worker_info(data):
    """ 执行设备被删除时的钩子 """

    worker = globals.get('worker')
    for index, item in enumerate(worker):
        if item.get('id') == data.get('id'):
            del worker[index]

    globals.add('worker', worker)
    logging.info('执行设备被删除')


@socket.on('masterDeviceEdit')
def edit_master_info(data):
    """ 控制设备信息更新时调用 """

    globals.add('master', data)
    globals.add('freeTask', True)
    logging.info(f'控制机 {data.get("name")} 信息更新')


@socket.on('workerDeviceEdit')
def edit_worker_info(data):
    """ 执行设备信息更新时调用 """

    worker = globals.get('worker')
    for index, item in enumerate(worker):
        if item.get('id') == data.get('id'):
            worker[index] = data
            break
    else:
        worker.append(data)

    globals.add('worker', worker)
    globals.add('freeTask', True)
    logging.info(f'执行机 {data.get("name")} 信息更新')
