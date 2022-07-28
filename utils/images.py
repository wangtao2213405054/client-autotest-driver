# _author: Coke
# _date: 2022/7/20 17:07

from PIL import Image

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
    image.save(infile)

    return infile


def cut(infile, area: tuple[int, int, int, int], aspect: tuple[int, int]) -> str:
    """
    对图片指定区域进行裁切并覆盖图片
    :param infile: 图片路径
    :param area: 裁切区域
    :param aspect: 宽高元组
    :return:
    """
    image = Image.open(infile)
    image = image.crop(area)

    result = Image.new('RGB', aspect)

    result.paste(image, area)
    result.save(infile)

    return infile
