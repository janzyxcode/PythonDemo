# _*_ coding: utf-8 _*_

import ngRequest
from io import BytesIO
import cv2
import numpy as np

def getCaptchaImge():
    urlStr = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.2347062926750'
    # response = session.get(urlStr, headers=headers)
    response = ngRequest.getRequest(urlStr)
    img = cv2.imread('/Users/liaonaigang/Downloads/AC28B28341202384728EF8DB964C13F7.png')
    cv2.show(img)
    # file = BytesIO(response.content)
    # cv2.im
    # img.show()


def captchaCheck():
    data = {
        "answer": 11,
        "login_site": "E",
        "rand": "sjrand"
    }

    url = "https://kyfw.12306.cn/passport/captcha/captcha-check"
    response = ngRequest.postRequest(url,data)
    print(response.status_code)
    print(response.text)


