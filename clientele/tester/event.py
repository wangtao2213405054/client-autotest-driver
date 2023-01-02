# _author: Coke
# _date: 2022/8/1 10:18

from clientele import drivers, api
import logging
import time


class CaseEvent(drivers.Driver):
    """
    测试用例事件统一入口
    方便 getattr 调用
    """

    def __init__(self, driver, wait=5):
        self.imagePaths = []
        self.images = []
        super().__init__(driver, wait)

    @staticmethod
    def show_wait(timer):
        """
        显示等待
        :param timer: 要等待的时间 s
        :return:
        """
        logging.info(f'等待 {timer} 秒')
        time.sleep(timer)

    def attribute(self, **kwargs): ...

    def url_screenshots(self):
        """ 继承 screenshots 方法后将图片上传至云端并返回 url 链接 """
        path = self.screenshots()
        url = api.upload_file(path).get('url')
        self.images.append(url)
        return url

    def save_screenshots(self, file_path: str = None, is_compression: bool = True) -> str:
        """
        重写 screenshots 方法, 并将图片地址存放在 imagePaths 中
        :param file_path:
        :param is_compression:
        :return:
        """
        path = self.screenshots(file_path, is_compression)
        self.imagePaths.append(path)
        return path
