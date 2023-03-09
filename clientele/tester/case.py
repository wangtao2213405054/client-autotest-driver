# _author: Coke
# _date: 2022/7/20 10:37

from clientele import api, utils, tester, drivers
from io import StringIO

import traceback
import logging.config
import logging
import time
import os


class TestCase(tester.CaseEvent):
    """ 用例组装器 """

    def __init__(self, driver, wait=5):
        """
        初始化函数, 需要一个用例事件的绑定对象
        :param driver: 本次启动的 driver
        """
        super().__init__(driver, wait)
        # 基础信息
        self.id = None  # 用例ID
        self.name = None  # 用例名称
        self.details = None  # 用例描述
        self.setList = []  # 所属集合
        self.module = None  # 用例模块
        self.priority = None  # 优先级
        self.status = None  # 用例状态 0 失败 1 成功 2 跳过
        self.output = StringIO()  # 本次用例执行过程中所产生的日志
        self.logger = logging.getLogger()

        # 错误信息
        self.errorStep = None  # 出错步骤的信息
        self.errorInfo = None  # 具体的错误原因
        self.errorDetails = None  # 原始错误

        # 图片相关
        self.images = []  # 运行过程中所产生的图片 url
        self.imagePaths = []  # 运行过程中所产出的图片路径
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
            caseId=self.id,
            name=self.name,
            details=self.details,
            module=self.module,
            setList=self.setList,
            priority=self.priority,
            output=self.output.getvalue(),
            images=self.images,
            status=self.status,
            errorStep=self.errorStep,
            errorInfo=self.errorInfo,
            errorDetails=self.errorDetails,
            gif=self.gif,
            startTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.startTime)),
            stopTime=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.stopTime)),
            duration=self.duration
        )
        return _fabric

    def assemble(self, step) -> classmethod:
        """
        将用例步骤中的函数进行映射, 如果未找到此关系映射则赋值一个空函数 attribute()
        :param step: 测试用例步骤的 item
        :return:
        """

        try:
            _attr = getattr(self, step.get('mapping'))
        except AttributeError:
            logging.warning(f'没有找到 {step.get("name")} 事件对应的函数映射, 请检查步骤事件配置是否正确')
            _attr = getattr(self, 'attribute')

        return _attr

    def run(self, case: dict):
        """
        执行测试用例
        :param case: 要执行的用例信息
        :return:
        """
        _pre = case.get('prePosition')  # 前置用例
        _post = case.get('postPosition')  # 后置用例
        steps = case.get('caseSteps', [])
        name = case.get('name')

        # 递归调用 执行前置用例
        if _pre:
            _case = api.get_case_info(_pre)
            self.run(_case)

        self.case(steps, name)

        # 递归调用，执行后置用例
        if _post:
            _case = api.get_case_info(_post)
            self.run(_case)

    def case(self, steps: dict, name: str) -> None:
        """ 执行测试用例步骤 """

        for index, item in enumerate(steps):
            steps_name = item.get('name', '')
            subset = item.get('subset', False)
            children = item.get('children', [])
            params = item.get('params', {})

            try:
                mapping = self.assemble(item)
                result = mapping(**params)

                # 如果方法存在子元素并且父元组判断为真, 则进行递归
                if subset and result:
                    self.case(children, steps_name)

                # 如果事件需要截图则进行截图
                if item.get('screenshot'):
                    self.save_screenshots()

            except Exception as error:
                self.errorStep = f'在执行 {name} 过程中的第 {index + 1} 个步骤: {steps_name} 时失败了'
                raise error

    def start(self, **kwargs):
        """ 调用此方法开始执行测试用例 """
        _id = kwargs.pop('id')
        if _id is None:
            return self.result

        case_info = api.get_case_info(_id)
        self.before(case_info)

        try:
            self.run(case_info)
        except Exception as e:
            logging.info(traceback.format_exc())
            self.errorDetails = traceback.format_exc()
            self.errorInfo = str(e)
            self.status = 0
            self.fail_screenshots()
        else:
            self.status = 1

        self.after()
        return self.result

    def fail_screenshots(self):
        """ 用例失败后进行截图 """
        try:
            self.url_screenshots()
        except Exception as e:
            logging.debug(e)

    def before(self, case_info):
        """ 在测试用例之前执行此方法 """
        self.id = case_info.get('id')
        self.name = case_info.get('name')
        self.details = case_info.get('desc')
        self.module = ' / '.join(case_info.get('moduleNameList'))
        self.priority = f'P{case_info.get("priority")}'
        self.setList = case_info.get('setNameInfo')

        # 将日志写入内存
        ch = logging.StreamHandler(self.output)
        self.logger.addHandler(ch)

    def after(self):
        """ 在测试用例结束后执行此方法 """

        self.stopTime = time.time()
        self.duration = round(self.stopTime - self.startTime, 2)

        # 测试结束后将生成的 GIF 图片上传至云端
        folder_path = utils.set_path('screenshots')
        file_path = os.path.join(folder_path, f"{int(time.time() * 1000)}.gif")
        if self.imagePaths:
            response = api.upload_file(utils.gif(self.imagePaths, file_path))
            self.gif = response.get('url') if response else None

        # 关闭应用进程
        self.quit()


if __name__ == '__main__':
    conf = dict(
        browser='Chrome',
        mockReset=False,
        url='http://localhost:9527/'
    )
    utils.logger(utils.INFO)
    obj = drivers.DriverStarter(**conf)
    test = TestCase(obj.selenium_starter)
    _result = test.start(id=1000000)
    print(_result)
