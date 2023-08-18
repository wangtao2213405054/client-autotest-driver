# _author: Coke
# _date: 2022/7/26 11:13

from typing import List, Dict
from clientele import utils, mock

import logging
import string
import os


class CreateMockCode:
    """ 创建 mock.py 代码 """

    instance = None

    def __new__(cls, url_list: List[Dict] = ()):
        if cls.instance is None:
            cls.instance = super(CreateMockCode, cls).__new__(cls)
            conf_path = utils.get_conf_path()
            _conf = utils.os.path.join(conf_path, 'mockCodeTemplate')
            with open(_conf, 'r', encoding='utf-8') as file:
                _code = file.readlines()

            cls._head = ''.join(_code[0: 40])
            cls._methods = ''.join(_code[40: 81])
            cls._logger = ''.join(_code[81: 86])

            cls.url_list = url_list

        return cls.instance

    def code(self, breakpoint_path: List[str] = ()) -> str:
        """
        用于生成 mitmproxy 所指定的 .py 脚本
        :return:
        """

        _methods = ''
        _logger = ''
        for index, item in enumerate(self.url_list):

            path = item.get('path')
            overall = item.get('overall')

            # 如果接口不为全局配置或者没有在拦截列表中时跳过
            if not overall and path not in breakpoint_path:
                continue

            record_request = item.get('recordRequest')
            record_response = item.get('recordResponse')
            breakpoint_request = item.get('breakpointRequest')
            breakpoint_response = item.get('breakpointResponse')

            _method = string.Template(self._methods)
            _class_name = mock.url_to_class(path)

            _code = _method.substitute(
                className=_class_name,
                url=path,
                recordRequest=record_request,
                recordResponse=record_response,
                breakpointRequest=breakpoint_request,
                breakpointResponse=breakpoint_response
            )
            _methods += _code

            _logger_class = f'    {_class_name}()'
            if index != len(self.url_list) - 1:
                _logger_class += ',\n'
            _logger += _logger_class

        _str = string.Template(self._logger)
        _logger = _str.substitute(add=_logger)

        _code = self._head + _methods + _logger

        logging.debug(f'本次创建 {len(self.url_list)} 个 mitmproxy 拦截器')
        return _code

    def create_file(self, filename: str = 'clientMockServiceCode.py', breakpoint_path: List[str] = ()) -> str:
        """
        创建 mitmproxy 指定脚本的 .py 文件
        :param filename: 要创建的文件名称
        :param breakpoint_path: 要注册到 mitmproxy 中的接口数据
        :return: 返回当前 mitmproxy 插件脚本的文件位置
        """

        folder_path = utils.set_path('mock')
        file_path = utils.os.path.join(folder_path, filename)
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(self.code(breakpoint_path))

        return file_path

    def create_api_info(self):
        """
        创建对应的 Json 文件
        :return:
        """
        request_breakpoint_path = utils.set_path('mock', 'breakpoint', 'request')
        response_breakpoint_path = utils.set_path('mock', 'breakpoint', 'response')
        utils.set_path('mock', 'record', 'request')
        utils.set_path('mock', 'record', 'response')

        for item in self.url_list:
            path = item.get('path')
            breakpoint_request = item.get('breakpointRequest')
            breakpoint_response = item.get('breakpointResponse')

            # 如果拦截请求为真则将数据写入到本地
            if breakpoint_request:
                file_path = os.path.join(request_breakpoint_path, f'{mock.url_to_class(path)}.json')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(item.get('request'))

            # 如果拦截响应为真则将数据写入到本地
            if breakpoint_response:
                file_path = os.path.join(response_breakpoint_path, f'{mock.url_to_class(path)}.json')
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(item.get('response'))
