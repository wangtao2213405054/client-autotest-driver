# _author: Coke
# _date: 2023/3/7 16:11

from typing import Any

import logging

_type = {
    'None': None,
    'Integer': int,
    'String': str,
    'Boolean': bool,
    'Array': list,
    'Object': dict,
    'Float': float
}

_condition = {
    '=': '==',
    '!=': '!=',
    '>': '>',
    '>=': '>=',
    '<': '<',
    '<=': '<=',
    'in': 'in',
    'out': 'not in'
}


def transition(value: str, types: str) -> Any:
    """
    将字符串转换为预期数据类型
    :param value: 要转换的值
    :param types: 要转换的类型
    :return: 返回转换后的数据, 如果转换失败则返回原有的值
    """

    try:
        shift = _type.get(types.capitalize())
        return shift(value) if shift is not None else None
    except (TypeError, ValueError):
        logging.info('数据转换失败, 请检查')
        return value


def operation(actual: Any, operator: str, expect: Any) -> bool:
    """
    通过运算返回运算结果, 运算失败或未识别的运算符返回为 False
    :param actual: 实际值
    :param operator: 运算条件
    :param expect: 预期值
    :return: 返回 True or False
    """

    operator = _condition.get(operator)

    actual = f"'{actual}'" if isinstance(actual, str) else actual
    expect = f"'{expect}'" if isinstance(expect, str) else expect

    try:
        if operator is None:
            raise TypeError

        execute = f'{actual} {operator} {expect}'
        result = eval(execute)
        logging.info(f'{execute} 运算结果为: {result}')
        return result

    except (SyntaxError, TypeError):
        return False


if __name__ == '__main__':
    print(operation(1, 'in', [1, 2]))
