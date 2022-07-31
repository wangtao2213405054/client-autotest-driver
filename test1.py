

import os
import threading
import time


def test():
    os.popen(r'python3 test2.py')


def test1():
    os.popen(r'python3 test3.py')


if __name__ == '__main__':
    thread = threading.Thread(target=test)
    thread1 = threading.Thread(target=test1)
    thread.start()
    thread1.start()
    print(thread1.is_alive())
    time.sleep(15)
    print(thread1.is_alive())