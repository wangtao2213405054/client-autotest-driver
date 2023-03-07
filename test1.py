
import multiprocessing
from clientele import utils, globals, tester, drivers
from io import StringIO
import logging
import time
import os
# test


# class TestCase(multiprocessing.Process):
#
#     def __init__(self, number, **kwargs):
#         self.number = number
#         super().__init__(**kwargs)
#
#     def run(self) -> None:
#         print(f'TestCase: {self.number}')


class Test(multiprocessing.Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self) -> None:
        pool = multiprocessing.Pool(processes=2)

        for item in range(5):
            pool.apply(runner) if not item else pool.apply_async(runner)

        pool.close()
        pool.join()


def runner():
    conf = dict(
        browser='Chrome',
        mockReset=False,
        url='http://localhost:9527/',
        platform='Web'
    )
    utils.logger(utils.INFO)
    obj = drivers.DriverStarter(**conf)
    _test = tester.TestCase(obj.run)
    _result = _test.start(id=1000000)


if __name__ == '__main__':
    obj1 = Test()
    obj1.start()
    obj1.join()
