# _author: Coke
# _date: 2022/11/18 15:22

from clientele.conf.env import env_map
from clientele import globals


import socketio

socket = socketio.Client(reconnection_delay=5)


def create_app():
    """
    创建 socket 链接
    :return:
    """

    _class = env_map.get(globals.get('environment'))
    socket.connect(_class.DOMAIN, {'token': globals.get('token')})
