# _author: Coke
# _date: 2023/3/8 10:50

from clientele import api


def get_project_info(data) -> api.request:
    """ 获取当前设备的信息 """

    return api.request(
        'GET',
        '/business/project/info',
        json=data
    )
