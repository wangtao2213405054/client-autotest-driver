# _author: Coke
# _date: 2022/7/20 17:41

import utils
import os

same_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def storage(*args: str, name='storage') -> str:
    """
    创建数据存储路径, 于项目同级目录
    如果更改存储路径 请在提交代码时将文件夹添加至 .gitignore 文件中过滤日志相关文件
    :param args: 要创建的文件夹, 多个文件夹会递归创建
    :param name: 基础文件夹名称
    :return:
    """

    storage_path = same_path
    base_folder = (name, utils.projectName, utils.device) + args
    for item in base_folder:
        storage_path = os.path.join(storage_path, item)
        if not os.path.exists(storage_path):
            os.mkdir(storage_path)

    return storage_path


def get_conf_path():
    """
    获取配置文件路径
    :return:
    """
    return os.path.join(same_path, 'conf')


if __name__ == '__main__':
    print(storage('message'))
