# _author: Coke
# _date: 2022/7/20 17:41

import os


def storage(folder, name='storage') -> str:
    """
    创建数据存储路径, 于项目同级目录
    :param folder: 要创建的文件夹
    :param name: 基础文件夹名称
    :return:
    """
    same_path = os.path.dirname(os.path.abspath('..'))
    storage_path = os.path.join(same_path, name)

    if not os.path.exists(storage_path):
        os.mkdir(storage_path)

    folder_path = os.path.join(storage_path, folder)
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)

    return folder_path


if __name__ == '__main__':
    storage('message')
