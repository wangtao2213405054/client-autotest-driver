# _author: Coke
# _date: 2022/7/26 22:41

from abc import abstractmethod

import threading
import platform
import warnings
import logging
import psutil
import socket
import time
import os
import re


def kill_port(port: int) -> None:
    """
    将占用端口号的进行关闭
    :param port: 端口号
    """
    _system = platform.system()

    if _system == 'Darwin' or _system == 'Linux':
        order = "lsof -i:%d | awk '{print $2}'" % port
        content_list = os.popen(order).readlines()
        for item in content_list:
            item = item.strip()
            if item.isdigit():
                _order = f'kill -9 {item}'
                logging.debug(f'关闭进程命令: {_order}')
                os.popen(_order)

    elif _system == 'Windows':
        # 修复 windows 下运行 kill 方法会关闭主进程的 bug
        course_info = os.popen(f'netstat -aon | findstr "{port}"').readlines()
        for item in course_info:
            item = item.strip()
            pid_list = re.findall(r'\d+$', item)
            if pid_list:
                _order = f'taskkill -t -f /pid {pid_list[0]}'
                logging.debug(f'关闭进程命令: {_order}')
                os.popen(_order)
                break

    else:
        warnings.warn('暂不支持的系统类型')
        return

    logging.debug(f'已关闭 {port} 端口进程')


def usage_port(ip: str, port: int) -> bool:
    """
    查看当前端口的占用情况, 如果占用则返回 True 否则为 False
    :param ip: ip 地址
    :param port: 端口号
    """
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _result = _socket.connect_ex((ip, port))
    logging.debug(f'{port} 端口处于 {"占用" if _result == 0 else "空闲"} 状态')
    return _result == 0


def get_host() -> str:
    """
    获取本机IP地址
    :return:
    """
    _ip = socket.gethostbyname(socket.gethostname())
    logging.debug(f'本机IP地址: {_ip}')
    return _ip


class GetSystemUtilities(threading.Thread):
    """ 获取当前设备的基本信息 """

    def __init__(self, interval=2, **kwargs):
        """
        重写 threading.Thread 类
        :param interval: 线程间隔时间
        :param kwargs: Thread class init params
        """
        super().__init__(**kwargs)
        self.cpu = dict(
            count=psutil.cpu_count(),
            logical=psutil.cpu_count(logical=False),
            percent=0.0
        )
        self.abort = True
        self.started = 0
        self.interval = interval

    def run(self) -> None:
        while self.abort:
            self.get_cpu_percent()
            self.reported()

    def get_cpu_percent(self) -> None:
        """ 获取 CPU 占用率"""
        self.cpu['percent'] = psutil.cpu_percent(interval=self.interval)

    def get_started_time(self) -> None:
        """ 获取开机时间 """
        self.started = int(psutil.users()[0].started)

    def stop(self) -> None:
        """
        停止线程
        :return:
        """
        logging.debug('线程停止')
        self.abort = False

    def restart(self) -> None:
        """
        重新启动
        :return:
        """
        logging.debug('线程重新启动')
        self.abort = True

    def start(self) -> None:
        """
        开始线程
        :return:
        """
        logging.debug('线程开始')
        super().start()

    def get_thread_status(self) -> bool:
        """
        获取当前线程运行状态
        :return: running true. stop false
        """
        return self.abort

    @property
    def get(self) -> dict:
        """
        获取当先类定义的系统数据
        :return:
        """
        return dict(
            cpu=self.cpu,
            startedTime=self.started
        )

    @abstractmethod
    def reported(self): ...


if __name__ == '__main__':
    from clientele import utils
    utils.logger(logging.DEBUG)
    obj = GetSystemUtilities(daemon=True)
    obj.start()
    obj.get_started_time()

    for items in range(20):
        time.sleep(2)
        if items == 5:
            obj.stop()
        print(obj.get)
