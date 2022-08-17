# _author: Coke
# _date: 2022/8/17 22:42


class ServerError(Exception):
    """ 服务异常 """

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        error_info = '服务异常'
        return self.message or error_info
