# _author: Coke
# _date: 2022/7/20 11:37


class DriverStarter:
    """ 启动器 """

    def __init__(self, **kwargs):
        ...

    def selenium_starter(self, url):
        """ selenium 启动器 """

        from selenium import webdriver

        driver = webdriver.Chrome()
        driver.get(url)

        return driver

    def appium_starter(self):
        """ appium 启动器 """

        from appium import webdriver

        driver = webdriver.Remote()

        return driver
