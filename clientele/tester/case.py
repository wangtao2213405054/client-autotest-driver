# _author: Coke
# _date: 2022/7/20 10:37

from io import StringIO

import logging
import time
import sys


class TestCase:
    """ 用例组装器 """

    def __init__(self, event):
        """
        初始化函数, 需要一个用例事件的绑定对象
        :param event: 用例事件对象
        """
        self.event = event

        # 基础信息
        self.name = None  # 用例名称
        self.details = None  # 用例描述
        self.module = None  # 用例模块
        self.priority = None  # 优先级
        self.status = None  # 用例状态
        self.output = StringIO()  # 本次用例执行过程中所产生的日志

        # 错误信息
        self.errorStep = None  # 出错步骤的信息
        self.errorInfo = None  # 具体的错误原因
        self.errorDetails = None  # 原始错误

        # 图片相关
        self.images = []  # 运行过程中所产生的图片 url
        self.imagePaths = []  # 运行过程中所产出的图片路口
        self.gif = None  # 本次运行时生成的 gif 步骤图

        # 本次 case 的时间
        self.startTime = time.time()  # 本次用例的开始时间
        self.stopTime = None  # 本次用例的结束时间
        self.duration = None  # 本次用例耗时

    @property
    def result(self) -> dict:
        """
        将本次运行 case 的结果组装
        :return:
        """
        _fabric = dict(
            name=self.name,
            details=self.details,
            module=self.module,
            priority=self.priority,
            output=self.output,
            images=self.images,
            errorStep=self.errorStep,
            errorInfo=self.errorInfo,
            errorDetails=self.errorDetails,
            gif=self.gif,
            startTime=self.startTime,
            stopTime=self.stopTime,
            duration=self.duration
        )
        return _fabric

    def assemble(self, case: list[dict]) -> list[dict]:
        """
        将用例步骤中的函数进行映射, 如果未找到此关系映射则赋值一个空函数 attribute()
        :param case: 用例的步骤列表
        :return:
        """
        for index, item in enumerate(case):
            try:
                _attr = getattr(self.event, item['function'])
            except AttributeError:
                logging.warning(f'没有找到 {item["name"]} 事件对应的函数映射, 请检查步骤事件配置是否正确')
                _attr = getattr(self.event, 'attribute')

            item['attr'] = _attr

        return case

    def run(self, case_id: int):
        self.start()

        _case = self.get_case(case_id)
        _steps = _case.get('case')

        # 递归调用
        _pre = _case.get('preposition')
        if _pre:
            self.run(_pre)

        try:
            for index, item in enumerate(_steps):
                ...
        except Exception as e:
            logging.debug(e)
            _class, _error, _traceback = sys.exc_info()

        self.stop()

    def start(self): ...

    def stop(self): ...

    def get_case(self, case_id) -> dict: ...
