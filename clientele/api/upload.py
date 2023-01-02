# _author: Coke
# _date: 2022/12/30 22:35

from clientele import api


def upload_file(path: str) -> dict:
    """ 获取测试用例信息 """

    if not path:
        return {}

    return api.request('POST', '/upload/file/image', files=dict(file=open(path, 'rb')))
