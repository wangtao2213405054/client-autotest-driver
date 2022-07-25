# _author: Coke
# _date: 2022/7/20 11:22


class ClickError(Exception):
    """ 点击异常类 """

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        error_info = '点击操作错误, 请检查'
        return self.message or error_info


class InputError(Exception):
    """ 输入异常类"""

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        error_info = '输入操作错误, 请检查'
        return self.message or error_info


class ClearError(Exception):
    """ 清空异常类 """

    def __init__(self, message=None):
        self.message = message

    def __str__(self):
        error_info = '清空异常, 请检查'
        return self.message or error_info
