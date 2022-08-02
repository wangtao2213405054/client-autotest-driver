# _author: Coke
# _date: 2022/8/2 15:30

from setuptools import find_packages, setup

setup(
    name='clientele',
    description='this is the client autotest platform driver',
    url='https://github.com/wangtao2213405054/client-autotest-driver',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'appium-python-client',
        'requests',
        'pillow',
        'selenium',
        'imageio'
    ]
)
