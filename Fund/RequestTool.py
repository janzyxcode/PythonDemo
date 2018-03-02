# _*_ coding: utf-8 _*_

import requests
import json
import time

# 一个提供UserAgent的库，不用自己再去搞那么多了，方便
from fake_useragent import UserAgent

# 禁用安全请求警告
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning
disable_warnings(InsecureRequestWarning)


__session = requests.session()
# 设置不验证SSL，你应该看到了HTTPS
__session.verify = False

__ua = UserAgent(verify_ssl=False)

# 请求头，最最基础的反爬伪装
__headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        "User-Agent": __ua.random,

        # "Referer": "https://kyfw.12306.cn/otn/login/init",
        # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        # "Accept": "application/json, text/javascript, */*; q=0.01"
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
    for i in range(10):
        try:
            return __session.get(urlStr, headers=__headers)
        except :
            if i >= 9:
                print('give up  ' + urlStr)
            else:
                time.sleep(0.5)
        else:
            time.sleep(0.05)
            break
    return None

# {"result_message":"系统维护时间","result_code":-4}
# {"result_message":"用户未登录","result_code":1}
def postRequest(urlStr,data):
    response = __session.post(urlStr, headers=__headers, data=data)
    if response.status_code == 200:
        return response.text



    return None

def clearCookies():
    __session.cookies.clear()