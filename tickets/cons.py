# _*_ coding: utf-8 _*_
import re
import urllib.request
import urllib.parse
import re
import json

# 广州南|IZQ
# 宾阳|UKZ
# 南宁东|NFZ
# 南宁|NNZ

cityNameDict = {}
cityCodeDict = {}


def getStationName():
    req = urllib.request.Request('https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9043')
    req.add_header('User-Agent','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36')
    html = urllib.request.urlopen(req).read()
    html = html.decode('utf-8')

    searchObj = re.match(r'(.*)station_names =\'(.*?)\';', html, re.I)
    str = searchObj.group(2)
    array = str.split('@')
    array.pop(0)
    for item in array:
        splis = item.split('|')
        cityNameDict[splis[1]] = splis[2]
        cityCodeDict[splis[2]] = splis[1]



def getCityNameWithCode(code):
    return cityCodeDict[code]

def getCityCodeWithName(name):
    return  cityNameDict[name]

