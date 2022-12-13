

import sys
import unittest
import traceback


try:
    raise IOError('test')
except Exception:
    print(traceback.format_exc())
