# _author: Coke
# _date: 2022/7/29 10:27

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
import smtplib
from clientele import utils
import os
import re


class Email:
    """ 邮件发送 """
    def __init__(self, mail_host, sender, password, receivers: list, title, **kwargs):
        """
        初始化 email 类
        :param mail_host: 邮箱服务器 如 QQ邮箱 smtp.qq.com
        :param sender: 用户名
        :param password: 授权码
        :param receivers: 接收人
        :param title: 邮件标题
        :param kwargs: 邮件模板需要替换的数据字典
        """
        self.mail_host = mail_host
        self.password = password
        self.sender = sender
        self.receivers = receivers
        self.title = title
        self.template = kwargs

    @property
    def style(self) -> str:
        """
        绘制 email 文件所展示的样式
        :return:
        """
        _conf = utils.get_conf_path()
        _template = os.path.abspath(os.path.join(_conf, 'emailTemplate'))

        with open(_template, 'r', encoding='utf-8') as file:
            template = file.read()

        for key, value in self.template.items():
            template = re.sub(key, value, template)

        return template

    def sendmail(self) -> None:
        """
        发送邮件
        :return:
        """
        _message = MIMEMultipart()
        _message['Subject'] = self.title
        _message['From'] = self.sender
        _message['To'] = ';'.join(self.receivers)

        param = MIMEText(self.style, 'html', 'utf-8')
        _message.attach(param)

        _smtp = smtplib.SMTP()
        _smtp.connect(self.mail_host, 25)
        _smtp.login(self.sender, self.password)
        _smtp.sendmail(self.sender, self.receivers, _message.as_string())
        _smtp.quit()


class DingTalk:
    """
    钉钉机器人封装
    详情请看钉钉开放平台官网: https://open.dingtalk.com/document/group/custom-robot-access
    """

    def __init__(self, token, mobile: list = None, user: list = None, own: bool = False):
        """
        发送钉钉机器人消息
        :param token: 群机器人的 Token
        :param mobile: 通过手机号 @ 群聊中的人 [mobile, ....]
        :param user: 通过用户id @ 群聊中的人 [id, ...]
        :param own: 是否 @ 所有人
        """
        self.url = f'https://oapi.dingtalk.com/robot/send?access_token={token}'
        self.body = {
                'at': dict(atMobiles=mobile, atUserIds=user, isAtAll=own)
            }

    def text(self, text: str) -> requests.request:
        """
        钉钉机器人 text 消息类型
        :param text: 要发送的文本信息
        :return:
        """
        self.body['text'] = dict(content=text)
        self.body['msgtype'] = 'text'
        return requests.request('POST', self.url, self.body)

    def link(self, title, text, url, image) -> requests.request:
        """
        钉钉机器人 link 消息类型
        :param title: 标题
        :param text: 内容
        :param url: 点击消息体跳转的 url
        :param image: 消息体中的图片
        :return:
        """
        self.body['link'] = dict(
            title=title,
            text=text,
            messageUrl=url,
            picUrl=image
        )
        self.body['msgtype'] = 'link'
        return requests.request('POST', self.url, self.body)

    def markdown(self, title, text) -> requests.request:
        """
        钉钉机器人 markdown 消息类型
        :param title: 标题
        :param text: 内容
        :return:
        """
        self.body['markdown'] = dict(
            title=title,
            text=text
        )
        self.body['msgtype'] = 'markdown'
        return requests.request('POST', self.url, self.body)

    def action(self, title, text) -> requests.request:
        """
        钉钉机器人 actionCard 消息类型
        :param title: 标题
        :param text: 内容
        :return:
        """
        self.body['actionCard'] = dict(
            title=title,
            text=text
        )
        self.body['msgtype'] = 'actionCard'
        return requests.request('POST', self.url, self.body)

    def feed(self, links) -> requests.request:
        """
        钉钉机器人 feedCard 消息类型
        :param links: 字典中需要包含 title, messageURL, picURL 字段
        :return:
        """
        self.body['feedCard'] = dict(links=links)
        self.body['msgtype'] = 'feedCard'
        return requests.request('POST', self.url, self.body)
