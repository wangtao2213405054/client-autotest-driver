# _author: Coke
# _date: 2022/7/26 22:41

import platform
import warnings
import logging
import socket
import os
import re


def kill_prot(prot: int) -> None:
    """
    将占用端口号的进行关闭
    :param prot: 端口号
    """
    _system = platform.system()

    if _system == 'Darwin' or _system == 'Linux':
        order = "lsof -i:%d | awk '{print $2}'" % prot
        content_list = os.popen(order).readlines()
        for item in content_list:
            item = item.strip()
            if item.isdigit():
                _order = f'kill -9 {item}'
                logging.debug(f'关闭进程命令: {_order}')
                os.popen(_order)

    elif _system == 'Windows':
        # 修复 windows 下运行 kill 方法会关闭主进程的 bug
        course_info = os.popen(f'netstat -aon | findstr "{prot}"').readlines()
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

    logging.debug(f'已关闭 {prot} 端口进程')


def usage_prot(ip: str, prot: int) -> bool:
    """
    查看当前端口的占用情况, 如果占用则返回 True 否则为 False
    :param ip: ip 地址
    :param prot: 端口号
    """
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _result = _socket.connect_ex((ip, prot))
    logging.debug(f'{prot} 端口处于 {"占用" if _result == 0 else "空闲"} 状态')
    return _result == 0


def get_host() -> str:
    """
    获取本机IP地址
    :return:
    """
    _ip = socket.gethostbyname(socket.gethostname())
    logging.debug(f'本机IP地址: {_ip}')
    return _ip


if __name__ == '__main__':
    print(get_host())
