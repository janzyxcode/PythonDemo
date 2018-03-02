# _*_ coding: utf-8 _*_


from aip import AipOcr
import wda
import cv2
import webbrowser
import time
import datetime
from urllib import parse
import numpy as np
import requests



# """ 你的 APPID AK SK """
APP_ID = '10701834'
API_KEY = 'TbOZqAG7Xu0HutH2hKGSSZOU'
SECRET_KEY = 'm3zG4I9KXqGnkhKcgWDxohQkMB5QqMLA'

client = AipOcr(APP_ID, API_KEY, SECRET_KEY)



# c = wda.Client('http://192.168.0.117:8100')
# s = c.session()
# print(s.window_size())


def printNowDatetime():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def getImage(url):
    with open(url,'rb') as fp:
        return fp.read()

def ocrImage(image):
    # image = getImage('/Users/user/Desktop/testP.png')

    """ 如果有可选参数 """
    options = {}
    options["language_type"] = "CHN_ENG"
    options["detect_direction"] = "true"
    options["detect_language"] = "true"
    options["probability"] = "true"

    """ 带参数调用通用文字识别, 图片参数为本地图片 """
    response = client.basicGeneral(image, options)
    print(response)
    print(type(response))
    words = response['words_result']
    appendWord = ''
    for item in words:
        appendWord += item['words'] + ''
    return appendWord


def cvCutImg(x,y,width,height,img):
    return img[y:y+height, x:x+width]

def cvBytes_to_numpyNdarray(imgBytes):
    img = np.asarray(bytearray(imgBytes), np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    # cv2.imshow('mm', img)
    # cv2.waitKey(0)

    # img type is numpy.ndarray
    # img = cv2.imread('/Users/user/Desktop/testP.png')
    return img

def cvNumpyNdarray_to_bytes(img):
    return np.ndarray.tobytes(img)


def chongdingdahui():
    img = c.screenshot('screen01.png')
    # img = getImage('chongdingdahui.jpg')
    image = cvBytes_to_numpyNdarray(img)
    cutImg = cvCutImg(25, 320, 700, 175, image)
    cv2.imwrite('cut.png', cutImg)
    image = getImage('cut.png')
    ocrwd = ocrImage(image)
    image = getImage('cut.png')
    ocrwd = ocrImage(image)
    wd = parse.quote(ocrwd)
    url = 'https://www.baidu.com/s?wd=' + wd
    webbrowser.open(url)


def xiguashiping():
    # img = c.screenshot('screen01.png')
    img = getImage('xiguaishipin.jpg')
    image = cvBytes_to_numpyNdarray(img)
    cutImg = cvCutImg(40, 220, 670, 175, image)
    cv2.imwrite('cut.png', cutImg)
    image = getImage('cut.png')
    ocrwd = ocrImage(image)
    image = getImage('cut.png')
    ocrwd = ocrImage(image)
    wd = parse.quote(ocrwd)
    url = 'https://www.baidu.com/s?wd=' + wd
    webbrowser.open(url)



if __name__ == "__main__":
    print('--')
    while True:
        time.sleep(3)
        printNowDatetime()
        # chongdingdahui()
        xiguashiping()














