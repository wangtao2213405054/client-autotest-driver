# _author: Coke
# _date: 2022/9/7 18:59

from typing import Any

memory = dict(
    projectName='client',
    device='iPhone',
    platform='ios',
    ports=[],
    environment='local'
)


def add(key: str, value: Any) -> None:
    """
    添加一个变量
    :param key:
    :param value:
    :return:
    """
    memory[key] = value


def get(key: str) -> Any:
    """
    获取变量值
    :param key:
    :return:
    """
    return memory.get(key)


def delete(key: str) -> None:
    """
    删除变量值
    :param key:
    :return:
    """

    del memory[key]


def clear() -> None:
    """
    清空变量值
    :return:
    """
    memory.clear()
