import importlib


if __name__ == '__main__':
    _module = importlib.import_module('utils.path')
    _function = getattr(_module, 'storage')
    _function('message')
