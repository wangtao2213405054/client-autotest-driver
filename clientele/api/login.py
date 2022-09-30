# _author: Coke
# _date: 2022/8/17 22:57

from clientele.api.request import request, sha1_secret
from clientele import globals


class Login:
    """ clientele 登录 """

    def __init__(self, username: str, password: str):
        self.username = username
        self.password = sha1_secret(password)

    def token(self) -> request:
        body = dict(
            username=self.username,
            password=self.password
        )
        response = request('POST', '/user/login', json=body)
        globals.add('token', response.get('token'))
        return response


if __name__ == '__main__':
    _login = Login('coke@qq.com', '123456')
    print(_login.token())
