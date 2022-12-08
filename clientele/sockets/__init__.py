# _author: Coke
# _date: 2022/11/18 15:22

from clientele.conf.env import env_map
from clientele import globals


import socketio

socket = socketio.Client()


def create_app(token):
    """
    创建 socket 链接
    :param token: 连接服务器的设备 Token
    :return:
    """
    globals.add('token', token)
    _class = env_map.get(globals.get('environment'))
    socket.connect(_class.DOMAIN, {'token': globals.get('token')})
