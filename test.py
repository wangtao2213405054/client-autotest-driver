
import multiprocessing


class Test:

    def __init__(self, name):
        self.name = name

    def run(self):
        print(self.name)


if __name__ == '__main__':
    obj = Test('coke')
    _s = multiprocessing.Process(target=obj.run)
    _s.start()
    import time
    time.sleep(4)
