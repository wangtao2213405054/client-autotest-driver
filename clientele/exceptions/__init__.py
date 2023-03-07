# _author: Coke
# _date: 2022/7/20 10:47

# 错误异常封装

from .driverError import ClickError, ClearError, InputError, FusingError
from .serverError import ServerError


__all__ = [
    'ClickError',
    'ClearError',
    'InputError',
    'ServerError',
    'FusingError'
]
