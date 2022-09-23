# _author: Coke
# _date: 2022/7/20 11:37

import logging


class DriverStarter:
    """ 启动器 """

    def __init__(self, **kwargs):
        self.device = kwargs

    @property
    def selenium_starter(self):
        """ selenium 启动器 """

        from selenium import webdriver
        _browser: str = self.device.get('browser')
        _mock = self.device.get('mockReset')
        _port = self.device.get('httpProxyPort')
        _head_reset = self.device.get('headReset')
        _url = self.device.get('url')

        if _browser.upper() == 'Chrome'.upper():
            chrome_options = webdriver.ChromeOptions()
            chrome_options.headless = _head_reset
            if _mock:
                chrome_options.add_argument(f'--proxy-server=http://127.0.0.1:{_port}')
            driver = webdriver.Chrome(options=chrome_options)

        elif _browser.upper() == 'Firefox'.upper():
            profile_config = {
                'network.proxy.type': 1,
                'network.proxy.http': '127.0.0.1',
                'network.proxy.http_port': _port,
                'network.proxy.ssl': '127.0.0.1',
                'network.proxy.ssl_port': _port
            }
            firefox_options = webdriver.FirefoxOptions()
            firefox_options.headless = _head_reset
            firefox_profile = webdriver.FirefoxProfile()

            for key, value in profile_config.items():
                firefox_profile.set_preference(key, value)
            firefox_profile.update_preferences()

            driver = webdriver.Firefox(
                firefox_profile=firefox_profile if _mock else None,
                options=firefox_options
            )

        else:
            _message = f'暂不支持的浏览器类型: {_browser}'
            logging.critical(_message)
            raise KeyError(_message)

        driver.get(_url)
        return driver

    @property
    def appium_starter(self):
        """ appium 启动器 """

        from appium import webdriver
        _port = self.device.get('appiumServerPort')
        driver = webdriver.Remote(f'http://localhost:{_port}/wd/hub', self.device)

        return driver

    @property
    def run(self):
        _platform: str = self.device.get('platform')
        if _platform.upper() == 'Web'.upper():
            return self.selenium_starter
        elif _platform.upper() == 'Android'.upper() or _platform.upper() == 'iOS'.upper():
            return self.appium_starter
        else:
            _message = f'暂不支持的运行平台: {_platform}'
            logging.critical(_message)
            raise KeyError(_message)
