# _author: Coke
# _date: 2022/12/30 22:35

from clientele import api


def upload_file(path: str) -> api.request:
    """ 获取测试用例信息 """

    return api.request(
        'POST',
        '/upload/file/image',
        files=dict(file=open(path, 'rb')),
        exceptions=Exception
    )
