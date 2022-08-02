# _author: Coke
# _date: 2022/7/28 15:32

from logging.handlers import RotatingFileHandler

import logging
from clientele import utils
import sys
import os

_LOG_BYTES = 1024 * 1024 * 100
_LOG_COUNT = 10

INFO = logging.INFO
DEBUG = logging.DEBUG
ERROR = logging.ERROR
WARNING = logging.WARNING
CRITICAL = logging.CRITICAL


def logger(level: INFO) -> None:
    """
    设置本次运行时的日志信息
    :param level: 日志等级
    :return:
    """
    _path = os.path.abspath(os.path.join(utils.storage('logs'), 'log.log'))
    # 日志格式
    formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s')

    # 设置存储文件 log
    log_handle = RotatingFileHandler(_path, maxBytes=_LOG_BYTES, backupCount=_LOG_COUNT)
    log_handle.setFormatter(formatter)

    # 设置控制台 log
    _handle = logging.StreamHandler(stream=sys.stdout)
    _handle.setFormatter(formatter)

    # 设置日志等级和全局信息
    logging.basicConfig(level=level, handlers=[_handle])
    logging.getLogger().addHandler(log_handle)


if __name__ == '__main__':
    logger(DEBUG)
    logging.error('Test')
