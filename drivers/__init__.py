# _author: Coke
# _date: 2022/7/20 10:46

# 驱动器
# 封装了 appium、selenium 相关的 api

from .appium import Appium
from .selenium import Selenium
from .driver import Driver
from .starter import appium_starter, selenium_starter

__all__ = [
    'Appium',
    'Selenium',
    'Driver',
    'appium_starter',
    'selenium_starter'
]
