# _author: Coke
# _date: 2022/8/17 22:56

from clientele.api.request import request
from typing import Tuple


def get_email(project_id) -> Tuple[bool, dict]:
    """
    获取邮箱列表
    :return: (switch, info) 返回邮件是否开启和邮件配置信息
    """
    body = dict(
        projectId=project_id
    )
    response = request('POST', '/message/email/info', json=body)
    params = dict(
        mail_host=response.get('host'),
        sender=response.get('sender'),
        password=response.get('password'),
        receivers=response.get('receivers'),
        title=response.get('title')
    )
    return response.get('state'), params


def get_talk(project_id) -> Tuple[bool, list]:
    """
    获取钉钉机器人配置
    :return: (switch, info) 返回钉钉机器人是否开启和配置信息
    """
    body = dict(
        projectId=project_id,
        app='talk'
    )
    response = request('POST', '/message/robot/info', json=body)
    robot_list = []
    for robot in response.get('tokens'):
        item_dict = dict(
            webhook=robot.get('token'),
            secret=robot.get('sign'),
            mobile=response.get('atMobile') if response.get('atAll') == 'part' else None,
            own=response.get('atAll') == 'yes'
        )
        robot_list.append(item_dict)

    return response.get('status'), robot_list


def get_lark(project_id) -> Tuple[bool, list]:
    """
    获取飞书机器人配置
    :return: (switch, info) 返回飞书机器人是否开启和配置信息
    """
    body = dict(
        projectId=project_id,
        app='lark'
    )
    response = request('POST', '/message/robot/info', json=body)
    robot_list = []
    for robot in response.get('tokens'):
        item_dict = dict(
            webhook=robot.get('token'),
            secret=robot.get('sign'),
        )
        robot_list.append(item_dict)

    return response.get('status'), robot_list
