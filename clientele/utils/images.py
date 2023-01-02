# _author: Coke
# _date: 2022/7/20 17:07

from PIL import Image
import imageio.v2 as imageio
from typing import Union

import logging
import os


def compress(infile, target=100, step=10, quality=80) -> str:
    """
    对图片进行压缩
    :param infile: 文件路径
    :param target: 压缩目标 KB
    :param step:  每次压缩的比率
    :param quality: 初始压缩比率
    :return:
    """

    if not os.path.isfile(infile):
        return infile

    file_size = os.path.getsize(infile)
    size = file_size / 1024

    while size > target:
        image = Image.open(infile)
        image.save(infile, quality=quality)

        if quality - step < 0:
            break

        quality -= step

    logging.debug(f'{infile} 图片 压缩至 {target} KB')

    return infile


def measure(infile, multiple) -> str:
    """
    调整图片尺寸
    :param infile: 图片路径
    :param multiple: 调整倍数
    :return:
    """
    image = Image.open(infile)

    width, height = image.size
    width *= multiple
    height *= multiple

    image = image.resize((int(width), int(height)), Image.ANTIALIAS)
    width, height = image.size
    image.save(infile)

    logging.debug(f'{infile} 图片尺寸调整为 {width}x{height}')

    return infile


def cut(infile, area: tuple, aspect: tuple[int, int]) -> str:
    """
    对图片指定区域进行裁切并覆盖图片
    :param infile: 图片路径
    :param area: 裁切区域 (int, int, int, int)
    :param aspect: 宽高元组
    :return:
    """
    image = Image.open(infile)
    image = image.crop(area)

    result = Image.new('RGB', aspect)

    result.paste(image, area)
    result.save(infile)

    logging.debug(f'已将{infile}图片 {area} 区域裁切')

    return infile


def gif(paths: list[str], infile: str, duration: int = 1.5) -> Union[str, None]:
    """
    将图片转换为 gif 动图
    :param paths: 要转换图片的列表
    :param infile: gif 图片的保存路径 .gif 结束
    :param duration: 图片切换的间隔
    :return:
    """

    if not paths:
        return

    frames = list(map(lambda x: imageio.imread(x), paths))
    imageio.mimsave(infile, frames, 'GIF', duration=duration)

    logging.debug(f'已将 {len(paths)} 张图片改变为动图')

    return infile


if __name__ == '__main__':
    gif([], r'D:\PycharmProject\client-autotest-driver\downloads\client\iPhone\test.gif')
