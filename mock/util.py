# _author: Coke
# _date: 2022/7/26 14:27


def url_to_class(value: str) -> str:
    """
    将 url 转换为 类名
    将 /api/v1/client/driver/get/token 转换为 _ApiV1ClientDriverGetToken
    :param value: 接口 url
    :return:
    """

    _class_name = '_'
    for items in value.split('/'):
        _class_name += ''.join(items.capitalize())

    return _class_name
