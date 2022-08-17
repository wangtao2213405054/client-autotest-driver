# _author: Coke
# _date: 2022/8/17 22:57

from clientele.api.request import request, sha1_secret
from clientele import utils


class Login:
    """ clientele 登录 """

    def __init__(self, username, password):
        self.username = username
        self.password = sha1_secret(password)

    def token(self):
        body = dict(
            username=self.username,
            password=self.password
        )
        response = request('POST', '/user/login', json=body)
        utils.token = response.get('token')
        return response


if __name__ == '__main__':
    _login = Login('coke@qq.com', '123456')
    print(_login.token())
    print(utils.token)
