# _*_ coding: utf-8 _*_

import wda
import numpy as np
import cv2
import webbrowser
from urllib import  parse
import requests
import datetime
import time

def cvBytes_to_numpyNdarray(imgBytes):
    # cutBytesImg = np.ndarray.tobytes(cutImg)
    img = np.asarray(bytearray(imgBytes), np.uint8)
    img = cv2.imdecode(img, cv2.IMREAD_COLOR)
    # cv2.imwrite('/Users/user/Desktop/testP22.png', img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    return img

def printNowDatetime():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 下面的文档中有session，client，element这些类的属性和方法
# https://github.com/openatx/facebook-wda/blob/master/wda/__init__.py



hostPath = 'http://192.168.0.119:8100'
c = wda.Client(hostPath)


def clientInfo():
    print(c.status())
    # {'state': 'success', 'os': {'name': 'iOS', 'version': '11.1.2'}, 'ios': {'simulatorVersion': '11.1.2', 'ip': '192.168.0.117'}, 'build': {'time': 'Jan  4 2018 16:36:23'}, 'sessionId': '88200B57-D9E6-4887-92AE-9FAF2F542EB8'}

    # Press home button
    c.home()

    # 暂时不懂
    c.healthcheck()

    # 返回UI手机当前界面UI的XML文件内容，锁屏情况下也会返回，但返回的是Home当前页的，如果UI越复杂，返回的越慢
    # 参数可传入 default false, True JSON
    pageUIXMLSource = c.source()
    print(pageUIXMLSource)

    # 截屏， 如果是当前处在app界面，会截取很快，在home状态会是很慢，也能截取lock
    screenImg = c.screenshot('screen01.png')
    # cvBytes_to_numpyNdarray(screenImg)



def SessionOperations():

    # 腾讯QQ
    # com.tencent.mqq
    # 微信
    # com.tencent.xin
    # 部落冲突
    # com.supercell.magic
    # 钉钉
    # com.laiwang.DingTalk
    # Skype
    # com.skype.tomskype
    # Chrome
    # com.google.chrome.ios

    # Open APP or close APP
    # s = c.session('com.apple.Health')

    s = c.session('com.ecwallet.jiafuletter')

    # One of <PORTRAIT | LANDSCAPE>
    print(s.orientation)  # expect PORTRAIT
    # s.orientation = wda.LANDSCAPE

    # s.close()
    print(s.bundle_id)
    print(s.id)
    print(s.window_size())

    wd = parse.quote('吃鸡')
    bdurl = 'https://www.baidu.com/s?wd=' + wd
    # 打开 手机Safari百度搜索吃鸡
    s = c.session('com.apple.mobilesafari', ['-u', bdurl])
    # 打开电脑浏览器百度搜索吃鸡
    result = webbrowser.open(bdurl)
    print(result)

    # printNowDatetime()
    # # Deactivate App for some time
    # s.deactivate(5.0)
    # printNowDatetime()

    s.tap(20, 250)
    s.double_tap(20, 250)


    # 从点1滑倒点2，时间默认为1s
    s.swipe(x1=200,y1=200,x2=200,y2=250,duration=0.5)
    s.swipe_left()
    s.swipe_down()
    s.swipe_right()
    s.swipe_up()

    s.tap_hold(20,250,1.0)

    # # Hide keyboard (not working in simulator), did not success using latest WDA
    # s.keyboard_dismiss()



def FindElement():
    s = c.session('com.ecwallet.jiafuletter')
    # Find element
    # Note: if element not found, WDAElementNotFoundError will be raised
    #
    # For example, expect: True or False
    # using id to find element and check if exists

    print(s(id="URL").exists)  # return True or False

    # using id or other query conditions
    print(s(id='URL').exists)
    print(s(name='URL').exists)
    print(s(text="URL").exists)  # text is alias of name
    print(s(nameContains='UR').exists)
    print(s(label='Address').exists)
    print(s(labelContains='Addr').exists)
    print(s(name='URL', index=1).exists)  # find the second element. index starts from 0

    # combines search conditions
    # attributes bellow can combines
    # :"className", "name", "label", "visible", "enabled"
    print(s(className='Button', name='URL', visible=True, labelContains="Addr").exists)
    print(s(name='猪').exists)
    print(s(className='Button', name='开始认证', label='开始认证', visible=True).exists)
    print('---')


    # More powerful findding method, XML
    s(xpath='//Button[@name="URL"]')
    s(classChain='**/Button[`name == "URL"`]')
    s(predicate='name LIKE "UR*"')
    s('name LIKE "U*L"')  # predicate is the first argument, without predicate= is ok



def ElementOperations():
    s = c.session('com.ecwallet.jiafuletter')
    source = c.source()
    print(source)
    # e = s(className='Button', name='立即登录', label='立即登录', visible=True)

    # Get first match Element object
    # The function get() is very important.
    # when elements founded in 10 seconds(:default:), Element object returns
    e = s(name='立即登录').get(timeout=9.0)
    # e.tap()
    print(e.bounds)
    print(e.bounds.x)

    # # Click element if exists
    # s(name='立即登录').click_exists(timeout=5)

    print(s(className='TextField',value='请输入手机号码').get(timeout=5).set_text('1111'))


def QQElementOperations():
    s = c.session('com.tencent.mqq')
    s.tap(175,650)
    printNowDatetime()
    # source = c.source()
    # print(source)
    print(s(className='ScrollView'))
    s(className='ScrollView').get(timeout=5).scroll('left',200)
    print('----')

def alert():
    s = c.session('com.tencent.mqq')
    print(s.alert.exists)
    print(s.alert.text)
    # s.alert.accept()  # Actually do click first alert button
    # s.alert.dismiss()  # Actually do click second alert button
    # s.alert.wait(5)  # if alert apper in 5 second it will return True,else return False (default 20.0)
    # s.alert.wait()  # wait alert apper in 2 second
    #
    # s.alert.buttons()
    # # example return: ["设置", "好"]
    #
    # s.alert.click("设置")

def weiboTest():
    s = c.session('com.sina.weibo')
    printNowDatetime()
    time.sleep(2)
    printNowDatetime()
    print(c.source())


if __name__ == "__main__":
    # QQElementOperations()
    # ElementOperations()
    # alert()
    weiboTest()