# _author: Coke
# _date: 2022/9/7 18:59

from typing import Any

import logging

memory = dict(
    projectName='client',
    device='iPhone',
    platform='ios',
    ports=[],
    environment='local',
    token='test',
    appId=''  # APP ID Android is appPackage iOS is BundleId
)


def add(key: str, value: Any) -> None:
    """
    添加一个变量
    :param key:
    :param value:
    :return:
    """
    if key in memory:
        logging.debug(f'{key} 变量已存在, 修改前信息{memory.get(key)}, 修改后信息: {value}')
    else:
        logging.debug(f'在 storage 中添加变量 {key}')
    memory[key] = value


def get(key: str) -> Any:
    """
    获取变量值
    :param key:
    :return:
    """
    logging.debug(f'获取 {key} 变量信息为: {memory.get(key)}')
    return memory.get(key)


def delete(key: str) -> None:
    """
    删除变量值
    :param key:
    :return:
    """
    if key in memory:
        logging.debug(f'已从内存中删除 {key}')
        del memory[key]
    else:
        logging.debug(f'{key} 不存在于内存变量之中')


def clear() -> None:
    """
    清空变量值
    :return:
    """
    logging.debug('清空内存变量')
    memory.clear()


def cover(data: dict) -> dict:
    """
    将传递过来的数据添加至变量中
    :param data: 需要写入的数据
    :return:
    """
    for key, value in data.items():
        add(key, value)

    return memory
