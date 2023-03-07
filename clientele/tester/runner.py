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
        :param runner: 指定的执行用例类
        """

        self.task_info = task_info
        self.device_info = device_info
        self.memory_info = memory_info
        self.token = memory_info.get('token', '')
        self.task_id = task_info.get('id')
        self.worker_id = device_info.get('id')
        self.start_conf = device_info.get('parsing', {})
        super().__init__(**kwargs)

    def run(self) -> None:
        """ 测试框架运行入口 """

        cases = self.task_info.get('cases', [])
        blocker = self.device_info.get('blocker', 3)
        globals.add('token', self.token)
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
        """ 执行进程 """
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

            for item in cases:
                params = (item, self.start_conf, memory)
                son = pool.apply(runner, args=params) if not item else pool.apply_async(runner, args=params)
                result.append(son)

            pool.close()
            pool.join()

        else:
            for item in cases:
                params = (item, self.start_conf)
                result.append(runner(*params))

        return list(map(lambda x: x.get() if isinstance(x, multiprocessing.pool.ApplyResult) else x, result))


def runner(case_id: int, conf: dict, manager=None) -> dict:
    """ 启动器的进程 """

    utils.logger(utils.INFO)

    # 如果为多进程模式则修改本地内存信息
    if manager:
        globals.memory = manager

    starter = drivers.DriverStarter(**conf)
    _actuator = tester.TestCase(starter.run)
    _result = _actuator.start(id=case_id)
    api.new_task_report(_result)

    return _result
