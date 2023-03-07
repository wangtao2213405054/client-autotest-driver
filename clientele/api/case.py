# _author: Coke
# _date: 2022/12/30 13:35

from clientele import api


def get_case_info(_id) -> api.request:
    """ 获取测试用例信息 """

    return api.request('POST', '/business/case/info', json=dict(id=_id))

