# _author: Coke
# _date: 2022/8/17 22:14

from clientele.conf.env import env_map
from clientele import globals, exceptions
from typing import Union, Dict, List

import requests
import logging
import hashlib


def request(method: str, uri: str, **kwargs) -> Union[Dict, List, str, int, None]:
    """
    基于 requests 库进行了二次业务封装
    所有跟 clientele 服务器做交互的库都应该调用此方法
    :param method: 请求类型
    :param uri:  请求的路径
    :return: 返回服务器返回消息体中的 data 数据
    """

    _class = env_map.get(globals.get('environment'))
    url = f'{_class.DOMAIN}{_class.PROFILE}{uri}'
    header = dict(
        token=globals.get('token')
    )

    response = requests.request(method, url, headers=header, **kwargs)
    if response.status_code != 200:
        _message = f'服务器内部错误, 状态码: {response.status_code}'
        logging.error(_message)
        raise exceptions.ServerError(_message)

    body = response.json()
    if body.get('code') != 1:
        _message = f'服务器响应错误, 错误信息: {body.get("msg")}'
        logging.error(_message)
        raise exceptions.ServerError(_message)

    return body.get('data')


def sha1_secret(secret: str) -> str:
    """
    使用sha1加密算法
    :return: 返回str加密后的字符串
    """

    sha = hashlib.sha1(secret.encode('utf-8'))
    encrypts = sha.hexdigest()
    return encrypts


if __name__ == '__main__':
    print(sha1_secret('123456'), type(sha1_secret('123456')))
