# _author: Coke
# _date: 2023/3/8 10:42

import pypinyin


def pinyin(_str):
    """ 将汉字转换为拼音 """

    _pinyin = ''
    for item in pypinyin.pinyin(_str, style=pypinyin.NORMAL):
        _pinyin += ''.join(item).capitalize()

    return _pinyin


if __name__ == '__main__':
    print(pinyin('Chrome'))
