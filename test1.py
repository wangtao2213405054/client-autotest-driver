
import multiprocessing
from clientele import utils, globals
from io import StringIO
import logging
import time
import os


class Test(multiprocessing.Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self) -> None:
        globals.clear()
        print(globals.memory, 'Test')


class Test1(multiprocessing.Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self) -> None:
        globals.add('token', 123)
        globals.add('Test1', 'this is Test process')
        print(globals.memory, 'Test1')


if __name__ == '__main__':
    utils.logger(utils.INFO)
    obj = Test(daemon=True)
    obj.start()
    obj1 = Test1(daemon=True)
    obj1.start()
    print(globals.memory, 'Main')
    time.sleep(5)
    print(globals.memory, '123321')
