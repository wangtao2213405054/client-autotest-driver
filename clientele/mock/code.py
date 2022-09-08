# _author: Coke
# _date: 2022/7/26 11:13

# 生成 mock.py 相关的代码

from clientele import utils, mock

import logging
import string


class CreateMockCode:
    """ 创建 mock.py 代码 """

    def __init__(self, url_list: list[str]):
        """
        初始化类数据, 并对部分数据进行赋值
        :param url_list: 所需要 mock 的 url 列表 [url, url]
        """
        conf_path = utils.get_conf_path()
        _conf = utils.os.path.join(conf_path, 'mockCodeTemplate')
        with open(_conf, 'r', encoding='utf-8') as file:
            _code = file.readlines()

        self._head = ''.join(_code[0: 23])
        self._methods = ''.join(_code[23: 34])
        self._logger = ''.join(_code[34:39])

        self.url_list = url_list

    @property
    def code(self) -> str:
        """
        用于生成 mitmproxy 所指定的 .py 脚本
        :return:
        """

        head_str = string.Template(self._head)
        _head = head_str.substitute(device=utils.get('device'))

        _methods = ''
        _logger = ''
        for index, item in enumerate(self.url_list):

            _method = string.Template(self._methods)
            _class_name = mock.url_to_class(item)

            _code = _method.substitute(class_name=_class_name, url=item)
            _methods += _code

            _logger_class = f'    {_class_name}()'
            if index != len(self.url_list) - 1:
                _logger_class += ',\n'
            _logger += _logger_class

        _str = string.Template(self._logger)
        _logger = _str.substitute(add=_logger)

        _code = _head + _methods + _logger

        logging.debug(f'本次创建 {len(self.url_list)} 个 mitmproxy 拦截器')
        return _code

    def create_file(self, filename='clientMockServiceCode.py') -> str:
        """
        创建 mitmproxy 指定脚本的 .py 文件
        :param filename: 要创建的文件名称
        :return: 返回当前 mitmproxy 插件脚本的文件位置
        """

        folder_path = utils.set_path('mock')
        file_path = utils.os.path.join(folder_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.code)

        return file_path


if __name__ == '__main__':
    obj = CreateMockCode(['/api/v1/platform/user/login', '/api/v1/platform/project/list'])
    print(obj.create_file())
