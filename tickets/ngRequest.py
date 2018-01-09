# _*_ coding: utf-8 _*_


import requests

# 一个提供UserAgent的库，不用自己再去搞那么多了，方便
from fake_useragent import UserAgent

# 禁用安全请求警告
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)


__session = requests.session()
__session.verify = False

__ua = UserAgent(verify_ssl=False)

# 请求头，最最基础的反爬伪装
__headers = {
    "User-Agent": __ua.random,
    "Host":"kyfw.12306.cn",
    "Referer":"https://kyfw.12306.cn/otn/passport?redirect=/otn/"
}

# class RequestSingleton(type):
#     _instance = {}
#     def __call__(cls, *args, **kwargs):
#         if cls._instance is None:
#             cls._instance = super(RequestSingleton, cls).__call__(*args,**kwargs)
#         return cls._instance
#
# class shared(metaclass=RequestSingleton):
#     pass


def getRequest(urlStr):
    return __session.get(urlStr, headers=__headers)

def postRequest(urlStr,data):
    return __session.post(urlStr, headers=__headers, data=data)