
import multiprocessing
import time
import os


class Test(multiprocessing.Process):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def run(self) -> None:
        start_time = time.monotonic()
        while start_time + 30 > time.monotonic():
            print(f'my name is son: {self.pid}')
            time.sleep(1)


if __name__ == '__main__':
    obj = Test(daemon=True)
    obj.start()
    end_time = time.monotonic()
    while end_time + 10 > time.monotonic():
        print(f'my name is father: {os.getppid()}')
        time.sleep(1)
