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
                kill(item)

    elif _system == 'Windows':
        # 修复 windows 下运行 kill 方法会关闭主进程的 bug
        course_info = os.popen(f'netstat -aon | findstr "{port}"').readlines()
        for item in course_info:
            item = item.strip()
            pid_list = re.findall(r'\d+$', item)
            if pid_list:
                kill(pid_list[0])
                break

    else:
        warnings.warn('暂不支持的系统类型')
        return

    logging.debug(f'已关闭 {port} 端口进程')


def kill(pid):
    """
    通过进程id关闭进程
    :param pid: 进程id
    :return:
    """
    _system = platform.system()
    if _system == 'Darwin' or _system == 'Linux':
        _order = f'kill -9 {pid}'

    elif _system == 'Windows':
        _order = f'taskkill -t -f /pid {pid}'

    else:
        warnings.warn('暂不支持的系统类型')
        return

    logging.debug(f'关闭进程命令: {_order}')
    os.popen(_order)


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

    def __init__(self, master, interval=1, **kwargs):
        """
        重写 threading.Thread 类
        :param master: 控制机 id
        :param interval: 线程间隔时间
        :param kwargs: Thread class init params
        """
        super().__init__(**kwargs)
        self.cpu = dict(
            count=psutil.cpu_count(),
            logical=psutil.cpu_count(logical=False),
            percent=0.00
        )
        self.abort = True
        self.started = ''
        self.interval = interval
        self.network = None
        self.virtual = None
        self.disk = None
        self.master = master

    def run(self) -> None:
        self.get_started_time()

        while self.abort:
            send, recv = self.get_network
            time.sleep(self.interval)
            self.get_cpu_percent()
            self.get_virtual_memory()
            self.get_disk()
            now_send, now_recv = self.get_network
            self.network = dict(
                send=round((now_send - send) / 1024, 2),
                recv=round((now_recv - recv) / 1024, 2)
            )
            self.reported()

    def get_cpu_percent(self) -> None:
        """ 获取 CPU 占用率"""
        self.cpu['percent'] = psutil.cpu_percent()

    def get_started_time(self) -> None:
        """ 获取开机时间 """
        self.started = time.strftime(
            '%Y-%m-%d %H:%M:%S',
            time.localtime(int(psutil.users()[0].started))
        )

    def get_virtual_memory(self) -> None:
        byte = 1024 * 1024 * 1024
        virtual = psutil.virtual_memory()
        self.virtual = dict(
            available=f'{virtual.available / byte:.2f}GB',
            total=f'{virtual.total / byte:.2f}GB',
            percent=virtual.percent
        )

    @property
    def get_network(self) -> tuple[int, int]:
        """ 获取网络信息 """
        return psutil.net_io_counters().bytes_sent, psutil.net_io_counters().bytes_recv

    def get_disk(self) -> None:
        """ 获取磁盘信息 """
        disk = psutil.disk_partitions()
        total = 0
        used = 0
        free = 0
        byte = 1024 * 1024 * 1024
        for item in disk:
            usage = psutil.disk_usage(item.mountpoint)
            total += usage.total
            used += usage.used
            free += usage.free
            if platform.system() != 'Windows':
                break

        self.disk = dict(
            total=f'{total / byte:.2f}GB',
            used=f'{used / byte:.2f}GB',
            free=f'{free / byte:.2f}GB',
            percent=round(used / total, 2)
        )

    def stop(self) -> None:
        """
        停止线程
        :return:
        """
        logging.debug('系统监控线程停止')
        if not self.abort:
            logging.debug('线程已停止... 请勿重复停止')
        self.abort = False

    def restart(self) -> None:
        """
        重新启动
        :return:
        """
        logging.debug('系统监控线程重新启动')
        if self.abort:
            logging.debug('线程正在运行中... 请勿重新启动')
        self.abort = True

    def start(self) -> None:
        """
        开始线程
        :return:
        """
        logging.debug('系统监控线程开始')
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
            id=self.master,
            cpu=self.cpu,
            startedTime=self.started,
            network=self.network,
            virtual=self.virtual,
            disk=self.disk,
            currentTime=time.strftime('%H:%M:%S')
        )

    @abstractmethod
    def reported(self) -> None:
        """
        继承此类后重写此方法，用于将系统监控信息上传
        :return:
        """


if __name__ == '__main__':
    kill_port(8081)
