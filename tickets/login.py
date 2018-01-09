# _*_ coding: utf-8 _*_

import ngRequest
from io import BytesIO
import numpy as np
import cv2



#https://prateekvjoshi.com/2016/03/01/how-to-read-an-image-from-a-url-in-opencv-python/
def getCaptchaImge():
    urlStr = 'https://kyfw.12306.cn/passport/captcha/captcha-image?login_site=E&module=login&rand=sjrand&0.2347062926750'
    # response = session.get(urlStr, headers=headers)
    response = ngRequest.getRequest(urlStr)
    arr = np.asarray(bytearray(response.content), dtype=np.uint8)
    img = cv2.imdecode(arr, cv2.IMREAD_COLOR)  # 'load it as it is'
    cv2.imshow('captchImge', img)
    cv2.waitKey(10)
    positions = input("input verify code:")



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


