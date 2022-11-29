# _author: Coke
# _date: 2022/8/2 16:15

from clientele.conf.env import env_map
from clientele import globals
from .api import *
from .drivers import *
from .mock import *
from .tester import *
from .utils import *
from .actuator import Actuator

import socketio

sio = socketio.Client()


def create_app(token):
    """
    创建 socket 链接
    :param token: 连接服务器的设备 Token
    :return:
    """
    globals.add('token', token)
    _class = env_map.get(globals.get('environment'))
    sio.connect(_class.DOMAIN, {'token': globals.get('token')})
