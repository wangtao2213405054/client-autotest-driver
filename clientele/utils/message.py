# _author: Coke
# _date: 2022/7/29 10:27

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from clientele import utils
from typing import Union, Tuple

import urllib.parse
import requests
import logging
import smtplib
import hashlib
import base64
import time
import hmac
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

        logging.debug(f'本次邮件接收人共 {len(self.receivers)} 位, 发送人为: {self.sender}')
        try:
            _smtp = smtplib.SMTP()
            _smtp.connect(self.mail_host, 25)
            _smtp.login(self.sender, self.password)
            _smtp.sendmail(self.sender, self.receivers, _message.as_string())
            _smtp.quit()
            logging.info('邮件发送成功')
        except Exception as e:
            logging.error(f'邮件发送失败: {e}')


class DingTalk:
    """
    钉钉机器人封装
    详情请看钉钉开放平台官网: https://open.dingtalk.com/document/group/custom-robot-access
    """

    def __init__(self, webhook, secret=None, mobile: list = None, user: list = None, own: bool = False):
        """
        发送钉钉机器人消息
        :param webhook: 群机器人的 webhook
        :param mobile: 通过手机号 @ 群聊中的人 [mobile, ....]
        :param user: 通过用户id @ 群聊中的人 [id, ...]
        :param own: 是否 @ 所有人
        """
        self.url = webhook
        self.body = {
            'at': dict(atMobiles=mobile, atUserIds=user, isAtAll=own)
        }
        if secret:
            timestamp, sign = self.sign(secret)
            self.url += f'&timestamp={timestamp}&sign={sign}'

    @staticmethod
    def sign(secret) -> Tuple[str, str]:
        """
        生成钉钉机器人签名
        :return: timestamp, sign
        """
        timestamp = str(round(time.time() * 1000))
        secret_enc = secret.encode('utf-8')
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        string_to_sign_enc = string_to_sign.encode('utf-8')
        hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
        sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
        return timestamp, sign

    @property
    def request(self):
        try:
            response = requests.request('POST', self.url, json=self.body, verify=False)
            if response.status_code != 200:
                logging.error(f'发送机器人信息失败, 服务状态码 "{response.status_code}"')
                return

            errcode = response.json().get('errcode')
            errmsg = response.json().get('errmsg')
            if errcode != 0:
                logging.error(f'发送机器人信息失败, 错误信息: {errmsg}')
                return

            logging.info('钉钉机器人消息发送成功')
            return response.json()

        except Exception as e:
            logging.error(f'发送机器人信息报错: {e}')

    def text(self, text: str) -> requests.request:
        """
        钉钉机器人 text 消息类型
        :param text: 要发送的文本信息
        :return:
        """
        self.body['text'] = dict(content=text)
        self.body['msgtype'] = 'text'
        return self.request

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
        return self.request

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
        return self.request

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
        return self.request

    def feed(self, links) -> requests.request:
        """
        钉钉机器人 feedCard 消息类型
        :param links: 字典中需要包含 title, messageURL, picURL 字段
        :return:
        """
        self.body['feedCard'] = dict(links=links)
        self.body['msgtype'] = 'feedCard'
        return self.request


class Lark:
    """
    飞书机器人封装
    详情请查看官方地址: https://open.feishu.cn/document/ukTMukTMukTM/ucTM5YjL3ETO24yNxkjN#d65d109d
    """

    def __init__(self, webhook, secret=None):
        self.url = webhook
        self.body = {}
        if secret:
            timestamp, sign = self.sign(secret)
            self.body['timestamp'] = timestamp
            self.body['sign'] = sign

    @staticmethod
    def sign(secret) -> Tuple[int, str]:
        # 拼接timestamp和secret
        timestamp = int(time.time())
        string_to_sign = '{}\n{}'.format(timestamp, secret)
        hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

        # 对结果进行base64处理
        sign = base64.b64encode(hmac_code).decode('utf-8')

        return timestamp, sign

    @property
    def request(self) -> Union[dict, None]:
        try:
            response = requests.request('POST', self.url, json=self.body, verify=False)

            if response.status_code != 200:
                logging.info(f'发送飞书通知错误, 状态码: {response.status_code}')
                return

            code = response.json().get('code')
            if code:
                logging.info(f'发送飞书通知错误, 错误信息: {response.json().get("msg")}')
                return

            logging.info('飞书机器人消息发送成功')
            return response.json()

        except Exception as e:
            logging.error(e)

    def text(self, text) -> request:
        self.body['msg_type'] = 'text'
        self.body['content'] = dict(text=text)
        return self.request

    def interactive(self, title, content, button_text, url) -> requests:
        self.body['msg_type'] = 'interactive'
        self.body['card'] = {}
        self.body['card']['config'] = {}
        self.body['card']['config']['wide_screen_mode'] = True

        self.body['card']['header'] = {}
        self.body['card']['header']['template'] = 'turquoise'
        self.body['card']['header']['title'] = {}
        self.body['card']['header']['title']['content'] = title
        self.body['card']['header']['title']['tag'] = 'plain_text'

        self.body['card']['i18n_elements'] = {}
        self.body['card']['i18n_elements']['zh_cn'] = []

        img = {'alt': {}, 'img_key': 'img_v2_bfd72a81-1533-4699-995d-12a675708d0g', 'tag': 'img'}
        img['alt']['content'] = ''
        img['alt']['tag'] = 'plain_text'

        div = {'tag': 'div', 'text': {}}
        div['text']['tag'] = 'lark_md'
        div['text']['content'] = content

        action = {'actions': [], 'tag': 'action'}
        actions = {'tag': 'button', 'text': {}, 'type': 'primary', 'url': url}
        actions['text']['content'] = button_text
        actions['text']['tag'] = 'plain_text'
        action['actions'].append(actions)

        for item in [img, div, action]:
            self.body['card']['i18n_elements']['zh_cn'].append(item)

        return self.request


if __name__ == '__main__':
    __message = Lark(
        'https://open.feishu.cn/open-apis/bot/v2/hook/4ba64e95-0820-46e9-8590-d1114f3d5420',
        'RZDTRhDXZkEGXTOQgBp8l'
    )
    __message.interactive('测试报告通知', '测试呀', '查看详情报告', 'https://www.baidu.com')
