# _author: Coke
# _date: 2022/7/20 10:36

from clientele import tester, drivers, utils, globals, api, exceptions

import multiprocessing
import traceback
import logging


class TestRunner(multiprocessing.Process):
    """ 测试执行器 """

    def __init__(self, task_info: dict, device_info: dict, memory_info: dict, **kwargs):
        """
        测试设备执行类
        :param task_info: 任务信息
        :param device_info: 执行设备信息
        :param memory_info: 共享信息
        """

        self.task_info = task_info
        self.device_info = device_info
        self.memory_info = memory_info
        self.token = memory_info.get('token', '')
        self.task_id = task_info.get('id')
        self.worker_id = device_info.get('id')
        self.start_conf = device_info.get('parsing', {})
        self.logging_level = device_info.get('logging', 'INFO')
        super().__init__(**kwargs)

    def run(self) -> None:
        """ 测试框架运行入口 """

        utils.logger(self.logging_level)
        logging.info(f'设备信息: {self.device_info}')
        logging.info(f'任务信息: {self.task_info}')
        logging.info(f'内存信息: {self.memory_info}')
        cases = self.task_info.get('cases', [])
        blocker = self.device_info.get('blocker', 3)
        globals.add('token', self.token)
        globals.add('device', f"{utils.pinyin(self.device_info.get('name'))}{self.device_info.get('id')}")
        globals.add('platform', self.device_info.get('platformName'))
        project_info = api.get_project_info(dict(
            id=self.task_info.get('projectId')
        ))
        globals.add('projectName', f"{utils.pinyin(project_info.get('name'))}{project_info.get('id')}")

        api.update_task_status(dict(
            id=self.task_id,
            status=1,
            device=self.worker_id
        ))

        api.update_worker_status(dict(id=self.worker_id, status=1))

        try:
            # 执行设备配置的阻断器, 如果未达成阻断条件则本次测试失败
            fusing = list(map(lambda x: False if not x.get('status') else True, self.process(cases[:blocker])))
            if True not in fusing:
                raise exceptions.FusingError

            self.process(cases[blocker:])

        except Exception as e:
            logging.info(e)
            logging.error(traceback.format_exc())
            api.update_task_status(dict(
                id=self.task_id,
                status=3,
                device=self.worker_id
            ))
            api.update_worker_status(dict(id=self.worker_id, status=2, cause=traceback.format_exc()))

        else:
            api.update_task_status(dict(
                id=self.task_id,
                status=2,
                device=self.worker_id
            ))
            api.update_worker_status(dict(id=self.worker_id, status=0))

    def process(self, cases: list) -> list[dict]:
        """
        执行测试用例列表, 并提供多进程的方式
        :param cases: 要执行的测试用例列表
        :return: 返回执行的测试用例结果
        """
        _platform = self.device_info.get('platformName')
        _concurrent = self.task_info.get('concurrent', False)
        _processes = self.task_info.get('processes', 5)

        result = []

        # 多进程模式
        if _concurrent and _platform.lower() == 'Web'.lower() and len(cases) > 1:
            pool = multiprocessing.Pool(processes=_processes)
            manager = multiprocessing.Manager()
            memory = manager.dict()
            for key, value in globals.memory.items():
                memory[key] = value

            for index, item in enumerate(cases):
                params = (item, self.start_conf, self.task_id, memory, self.logging_level)
                son = pool.apply(runner, args=params) if not index else pool.apply_async(runner, args=params)
                result.append(son)

            pool.close()
            pool.join()

        else:
            for item in cases:
                params = (item, self.start_conf, self.task_id)
                result.append(runner(*params))

        return list(map(lambda x: x.get() if isinstance(x, multiprocessing.pool.ApplyResult) else x, result))


def runner(case_id: int, conf: dict, task_id, manager=None, level=None) -> dict:
    """
    启动测试任务, 并执行测试用例
    :param case_id: 用例ID
    :param conf: 设备配置
    :param task_id: 任务ID
    :param manager: 是否为多进程模式
    :param level: 日志等级, 非多进程可忽略
    :return: 返回用例执行的结果
    """

    # 如果为多进程模式则修改本地内存信息
    if manager:
        globals.memory = manager
        utils.logger(level)

    starter = drivers.DriverStarter(**conf)
    _actuator = tester.TestCase(starter.run)
    _result = _actuator.start(id=case_id)
    _result['id'] = task_id
    logging.debug(_result)
    api.new_task_report(_result)

    return _result
