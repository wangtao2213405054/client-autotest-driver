import importlib
import inspect
from clientele.drivers import Appium


if __name__ == '__main__':
    _module = importlib.import_module('drivers.appium')
    mo = inspect.getmembers(_module)
    for item in mo:
        name, obj = item
        if inspect.isclass(obj):
            print(name)

        if inspect.ismethod(obj):
            print(name)

    _class = getattr(_module, 'Appium')
    print(_class, Appium)
    _function = getattr(_class, 'find_elements')

    print(_function)
    _function('2', 'v')
