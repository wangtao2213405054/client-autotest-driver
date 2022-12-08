
import os
import time
from clientele import kill
pid = os.getpid()
print('pid : ', pid)
kill(pid)

time.sleep(10)
