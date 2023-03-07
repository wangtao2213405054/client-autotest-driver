# _author: Coke
# _date: 2022/8/17 22:20


class Base:

    DOMAIN = 'http://127.0.0.1:5000'
    PROFILE = '/api/v1/client'


class Local(Base):
    """ 本地环境 """


class Daily(Base):
    """ 测试环境 """
    DOMAIN = 'http://101.42.24.232/'


class Public(Base):
    """ 正式环境 """


env_map = {
    'local': Local,
    'daily': Daily,
    'public': Public
}
