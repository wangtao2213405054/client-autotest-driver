# _author: Coke
# _date: 2022/7/20 11:46

from .util import *
from .code import CreateMockCode
from .server import start_mitmproxy_server
from .alter import reset_value

# 这是 mock http 接口的封装方法
# 如果你需要使用此功能 请安装 mitmproxy 工具
# windows 安装 8.x 及以上版本
# mac or linux 安装 6.0.2 版本
# 如果安装较高版本, 可能会导致过滤域名不生效, 及为 iPhone 手机安装包安装完成后会需要信任,
# 版本过高可能导致无法过滤 apple 相关的数据, 进而导致安装失败等情况...
# 在 windows 上不受影响
# 如果你的项目需要使用此 mock 功能, 那么你需要安装 mitmproxy 相关证书并信任
# android 8.x 以上的版本安装证书时无法生效, 需要对手机进行 root
# 证书的安装类似于 Charles, 访问 mitmproxy.org 即可查看安装及配置相关文档
# 使用 mock 服务的项目运行时请注意手机需要添加代理


__all__ = [
    'CreateMockCode',
    'url_to_class',
    'start_mitmproxy_server',
    'reset_value'
]
