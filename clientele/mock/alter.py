# _author: Coke
# _date: 2022/7/26 11:17

# 对 mock 的数据进行更新

from clientele import utils, mock

import logging
import json
import os


def reset(url, value, coord: list[str]):
    """
    重新设置 json 中对应坐标的 value
    :param url: 接口 url
    :param value: 要修改的值
    :param coord: 要修改的字段
    :return:
    """

    url = mock.url_to_class(url)
    file_folder = utils.set_path('mock')
    file_path = os.path.join(file_folder, f'{url}.json')

    # 修改文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        _response = json.loads(file.read())

    # 获取 坐标
    new_data = [_response]

    for i, key in enumerate(coord):
        # 將 list index 转换为 int
        if not isinstance(key, int):
            if key.isdigit():
                key = int(key)

        _response = _response[key]
        if i == len(coord) - 2:
            new_data.append(_response)

    # 倒序 坐标
    coord.reverse()
    new_data.reverse()

    # 修改目标 value
    new_data[0][coord[0]] = value

    # 返回修改后的 json
    data = new_data[-1]

    # 将信息写入
    update_data = json.dumps(data, ensure_ascii=False, indent=2)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(update_data)

    logging.info(f'已将 {url} 接口中的 {new_data[0][coord[0]]} 值修改为: {value}')

    return data


if __name__ == '__main__':
    data_list = ["data", 'serviceStats', 0, 'title']
    data1_list = ['message']
    _url = '/api/v1/client/mock/test'
    print(reset(_url, '哈哈哈333', data_list))
