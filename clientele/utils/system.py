# _author: Coke
# _date: 2022/7/26 22:41

import platform
import warnings
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
                os.popen(f'kill -9 {item}')

    elif _system == 'Windows':
        # 修复 windows 下运行 kill 方法会关闭主进程的 bug
        course_info = os.popen(f'netstat -aon | findstr "{prot}"').readlines()
        for item in course_info:
            item = item.strip()
            pid_list = re.findall(r'\d+$', item)
            if pid_list:
                os.popen(f'taskkill -t -f /pid {pid_list[0]}')
                break

    else:
        warnings.warn('暂不支持的系统类型')


def usage_prot(ip: str, prot: int) -> bool:
    """
    查看当前端口的占用情况, 如果占用则返回 True 否则为 False
    :param ip: ip 地址
    :param prot: 端口号
    """
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _result = _socket.connect_ex((ip, prot))

    return _result == 0


def get_host() -> str:
    """
    获取本机IP地址
    :return:
    """
    return socket.gethostbyname(socket.gethostname())


if __name__ == '__main__':
    print(get_host())
