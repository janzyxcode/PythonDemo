# _*_ coding: utf-8 _*_
import RequestTool
import json
import re
import pymysql
import datetime
from multiprocessing import Pool
import sqlMgr

# 1.主题持仓股票   持仓统计截止日期
# http://fund.eastmoney.com/api/FundTopicInterface.ashx?dt=15&sort=CYBL&sorttype=desc&tt=5ab8d1eb90748855&time=2017-12-31&pageindex=1&pagesize=10&callback=jQuery1830005206687565519452_1517662406251&_=1517664977489

todayStr = datetime.datetime.now().strftime("%Y-%m-%d")


def executeSql(sql):
    sqlMgr.cur.execute(sql)
    sqlMgr.conn.commit()
    # try:
    #     sqlMgr.cur.execute(sql)
    #     sqlMgr.conn.commit()
    # except:
    #     sqlMgr.conn.rollback()

def jsonFormtPrint(dic):
    print(json.dumps(dic,sort_keys=True,indent=2,ensure_ascii=False))


def decoFund(result,topicId,topicName,fundInfoDic,topicKey):
    series = result['series']
    fundScale = 0
    if len(series) > 0:
        fundScale = series[len(series) - 1]['y']

    sql = "INSERT INTO  fundOfTopic(date,topicId,topicName,fundId,TTYPE,TTYPENAME,FCODE,SHORTNAME,PDATE,FTYPE,fundScale,topicKey)" \
          "VALUES(str_to_date(\'%s\','%%Y-%%m-%%d'),\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%f,\'%s\')" \
          % (todayStr, topicId, topicName, fundInfoDic['_id'], fundInfoDic['TTYPE'], fundInfoDic['TTYPENAME'].strip(),
             fundInfoDic['FCODE'], fundInfoDic['SHORTNAME'], fundInfoDic['PDATE'], fundInfoDic['FTYPE'], fundScale,
             topicKey)
    executeSql(sql)


def getOneFund(num,topicId,topicName,fundInfoDic,topicKey):
    timeStr = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    url = 'http://fund.eastmoney.com/pingzhongdata/' + num + '.js?v=' + timeStr
    response = RequestTool.getRequest(url)
    if response != None and response.status_code == 200:
        # searchObj = re.search(r'(\s)var stockCodes=\[(.*?)\];(.*)var zqCodes="(.*?)";(.*)var Data_fluctuationScale =('r'.*?);(.*)/*持有人结构(.*)',response.text, re.I|re.S)
        # 基金持仓股票代码
        # stockCodes = searchObj.group(2)
        # stockCodeList = stockCodes.split(',')
        # for item in stockCodeList:
        #    if len(item) > 0:
        #        sql = "INSERT INTO  fundStockCodes(date,fcode,code,topicKey)" \
        #            "VALUES(str_to_date(\'%s\','%%Y-%%m-%%d'),\'%s\',\'%s\',\'%s\')" \
        #            % (todayStr, num, item[1:len(item) - 1],topicKey)
        #        executeSql(sql)
        #
        # # 基金持仓债券代码
        # zqCodes = searchObj.group(4)
        # zqCodeList = zqCodes.split(',')
        # for item in zqCodeList:
        #    if len(item):
        #        sql = "INSERT INTO  fundZqCodes(date,fcode,code,topicKey)" \
        #            "VALUES(str_to_date(\'%s\','%%Y-%%m-%%d'),\'%s\',\'%s\',\'%s\')" \
        #            % (todayStr, num, item,topicKey)
        #        executeSql(sql)

        # # 规模变动 mom-较上期环比
        scaleSearch = re.search(
            r'(.*)var Data_fluctuationScale =('r'.*?);(.*)/*持有人结构(.*)',
            response.text, re.I | re.S)
        if scaleSearch != None:
            reslut = scaleSearch.group(2)
            if isinstance(reslut, str):
                dic = json.loads(reslut)
                if isinstance(dic, dict):
                    decoFund(dic, topicId, topicName, fundInfoDic, topicKey)
                    return None

            if isinstance(reslut, dict):
                decoFund(reslut, topicId, topicName, fundInfoDic, topicKey)




# 获取某主题下的基金
def getFundsOfTopic(topicId,topicName,topicKey,pageindex):
    # "_id": "5ab8d1eb90748855004597",
    # "TTYPE": "5ab8d1eb90748855",
    # "TTYPENAME": "银行",
    # "FCODE": "004597", // 编号
    # "SHORTNAME": "南方银行ETF联接A",
    # "PDATE": "2018-02-02", // 更新
    # "FTYPE": "联接基金"

    # v=0.8371878028540056'
    url = 'http://fund.eastmoney.com/api/FundTopicInterface.ashx?callbackname=topicFundData&sort=SYL_6Y&sorttype=DESC&ft=&pageindex=' + str(pageindex) + '&pagesize=10&dt=10&tp=' + topicId
    response = RequestTool.getRequest(url)
    if response != None and response.status_code == 200:
        searchObj = re.match(r'(.*)var topicFundData={(.*?)"Pages":(.*?)}', response.text, re.I)
        resultStr = '{' + searchObj.group(2) + '"Pages":' + searchObj.group(3) + '}'
        resultDic = json.loads(resultStr)
        totalCount = resultDic['TotalCount']
        datas = resultDic['Datas']

        for item in datas:
            # print(item['SHORTNAME'])
            getOneFund(item['FCODE'], topicId, topicName, item, topicKey)

        if totalCount > pageindex * 10:
            getFundsOfTopic(topicId, topicName, topicKey, pageindex + 1)


# 获取某主题相关的信息
def getTopicInfo(topicId,gainState,type,totalCount,topicKey,gain):
    # "TType": "5ab8d1eb90748855",
    # "TTypeName": "银行",
    # "pdate": "2018-02-02", // 更新日期
    # "D": -0.3521, // 上一天涨幅
    # "DRANK": 262, // 上一天排名
    # "DSC": 266, // 上一天排名主题数
    # "W": -0.0431, // 近1周涨幅
    # "WRANK": 6, // 进1周排名
    # "WSC": 266, // 近1周排名主题数
    # "M": 11.0318, // 近1月涨幅
    # "MRANK": 1, // 近1月排名
    # "MSC": 266, // 近1月排名主题数
    # "Q": 14.8211, // 近3月涨幅
    # "QRANK": 1, // 近3月排名
    # "QSC": 266, // 近3月排名主题数
    # "HY": 12.2191, // 近6月涨幅
    # "HYRANK": 39, // 近6月排名
    # "HYSC": 266, // 近6月排名主题数
    # "Y": 26.5948, // 近1年涨幅
    # "YRANK": 26, // 近1你拿排名
    # "YSC": 266, // 近1年排名主题数

    url = 'http://fund.eastmoney.com/api/FundTopicInterface.ashx?callbackname=HeadData&dt=12&tp=' + topicId
    response = RequestTool.getRequest(url)
    if response != None and response.status_code == 200:
        searchObj = re.match(r'(.*)var HeadData={(.*?)}', response.text, re.I)
        resultStr = '{' + searchObj.group(2) + '}'
        resultDic = json.loads(resultStr)

        sql = "INSERT INTO  allTopics(date,gainState,type,totalCount,topicKey,topicId,TType,TTypeName,pdate,D,DRANK,DSC,W,WRANK,WSC,M,MRANK,MSC,Q,QRANK,QSC,HY,HYRANK,HYSC,Y,YRANK,YSC,gain,TopicType,IsQDII)" \
                    "VALUES(str_to_date(\'%s\','%%Y-%%m-%%d'),\'%s\',\'%s\',%d,\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',%f,%d,%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,%f,%d,%d,%f,%d,%d)" \
                    % (todayStr, gainState, type, int(totalCount), topicKey,topicId,resultDic['TType'],resultDic['TTypeName'].strip(),resultDic['pdate'],resultDic['D'],resultDic['DRANK'],resultDic['DSC'],resultDic['W'],resultDic['WRANK'],resultDic['WSC'],resultDic['M'],resultDic['MRANK'],resultDic['MSC'],resultDic['Q'],resultDic['QRANK'],resultDic['QSC'],resultDic['HY'],resultDic['HYRANK'],resultDic['HYSC'],resultDic['Y'],resultDic['YRANK'],resultDic['YSC'],gain,int(resultDic['TopicType']),bool(resultDic['IsQDII']))
        executeSql(sql)



def splitReq(loc, endLoc, datas,gainState,type,totalCount,topicKey):
    for i in range(loc,endLoc):
        item = datas[i]
        array = str(item).split(',')
        topicId = array[0]
        topicName = array[1]
        gain = float(array[2])

        print('start topicName：' + topicName)
        getFundsOfTopic(topicId, topicName, topicKey, 1)
        getTopicInfo(topicId, gainState, type, totalCount, topicKey, gain)



def addToPool(datas,gainState, gainType, totalCount, topicKey):
    datasLen = len(datas)
    section = 3
    p = Pool(section)
    if datasLen > 0:
        row = int(datasLen / section)
        left = 0
        if datasLen % 11 != 0:
            left = datasLen - row * section
        for i in range(0, section):
            if i == section - 1:
                # print(str(i * row) + '  ' + str(datasLen))
                p.apply_async(splitReq, args=(i * row, datasLen, datas, gainState, gainType, totalCount, topicKey))
            else:
                # print(str(i * row) + '  ' + str(i * row + row))
                p.apply_async(splitReq,
                              args=(i * row, i * row + row, datas, gainState, gainType, totalCount, topicKey))
    p.close()
    p.join()



searchList = ['沪港深', '房地产', '生物识别', '新能源车', '银行', '5G概念', '国际原油', '保险', '黄金概念', '新能源', '贵金属', '上证50', '消费', '酿酒行业', '创业板']

def removeNotIntList(list,topicKey):
    for name in list:
        # print(name)
        sql = "DELETE FROM fundOfTopic WHERE TTYPENAME = '" + name + "'" + " and topicKey = '" + topicKey + "'"
        executeSql(sql)



# 按阶段、类别、日期获取全部主题
def getAllTopic(gainState,type,dateStr,isAllStartSave):
    # 涨幅阶段  SYL_1N：1年   SYL_6：6个月  SYL_3：3个月   SYL_Y：1个月   SYL_Z：一周   SYL_D：1日
    # 板块类别  0：全部   1：综合指数  2：行业   3：概念  4：地区   5：含QDII的主题
    sorttype = 'desc'
    pageindex = '1'
    pagesize = '500'
    topicKey = dateStr + gainState + type

    pre = 'http://fund.eastmoney.com/api/FundTopicInterface.ashx?callbackname=fundData&sort='
    url = pre + gainState + '&sorttype=' + sorttype + '&pageindex=' + pageindex + '&pagesize=' + pagesize + '&dt=11&tt=' + type + '&rs=WRANK'
    response = RequestTool.getRequest(url)
    if response != None and response.status_code == 200:
        searchObj = re.match(r'(.*)var fundData={ (.*?)}', response.text, re.I)
        resultStr = '{' + searchObj.group(2) + '}'
        resultDic = json.loads(resultStr)
        totalCount = resultDic['TotalCount']
        datas = resultDic['Datas']
        datasLen = len(datas)
        print('topic len - ' + str(datasLen))

        if isAllStartSave:
            addToPool(datas,gainState,type,totalCount,topicKey)
            # section = 8
            # p = Pool(section)
            # if datasLen > 0:
            #     row = int(datasLen / section)
            #     left = 0
            #     if datasLen % 11 != 0:
            #         left = datasLen - row * section
            #     for i in range(0, section):
            #         if i == section - 1:
            #             # print(str(i * row) + '  ' + str(datasLen))
            #             p.apply_async(splitReq, args=(i * row, datasLen, datas, gainState, type, totalCount, topicKey))
            #         else:
            #             # print(str(i * row) + '  ' + str(i * row + row))
            #             p.apply_async(splitReq,
            #                           args=(i * row, i * row + row, datas, gainState, type, totalCount, topicKey))
            #
            # p.close()
            # p.join()


        else:
            notInList = []
            removeList = []
            sqlTopics = sqlMgr.readAllTopic(topicKey)
            for item in datas:
                array = str(item).split(',')
                topicName = array[1].strip()
                if isinstance(sqlTopics, list):
                    if topicName not in sqlTopics and topicName in searchList:
                        notInList.append(item)
                        removeList.append(topicName)
            if len(notInList) > 0:
                removeNotIntList(removeList,topicKey)
                addToPool(notInList, gainState, type, totalCount, topicKey)



# 轮询全部的主题
def runloopAllTopic():
    gainStates = ['SYL_D','SYL_Z','SYL_Y','SYL_3','SYL_6','SYL_1N']
    types = ['0']
    isAllStartSave = False
    for gainstate in gainStates:
        for type in types:
            print(gainstate)
            getAllTopic(gainstate,type,todayStr,isAllStartSave)



if __name__ == '__main__':
    print('start time -- ' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    runloopAllTopic()
    print('end time -- ' + datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
    sqlMgr.close()

