# _*_ coding: utf-8 _*_

import json

caseLock = False
requiredLok = True


modelStr = ''

def startWord():
    with open('/Users/user/Desktop/PythonDemo/CreateSwiftClass/NGSwiftJson','r',encoding='utf-8') as file_obj:
        data = json.load(file_obj)
        # print(json.dumps(data,indent=4,ensure_ascii=False))
        encodeJson(data,'')

def encodeJson(data,dicKey):
    if isinstance(data,list):
        first = data[0]
        encodeJson(first,dicKey)
    elif isinstance(data,dict):
        encodeDict(data,dicKey)
    else:
        return

def encodeDict(dic,dicKey):
    print('---- ' + str(dicKey) + ' ----')
    global modelStr
    modelStr += '\n' + str(dicKey) + 'Model：\n'
    keyTypes = []
    keyIfIndexDic = {}

    for key in dic.keys():
        value = dic[key]
        strKey = str(key)
        # print('key: ' + strKey + '：' + str(type(value)) + '   ' + str(value))
        if isinstance(value,list):
            encodeJson(value,strKey)
            modelStr += '    var : [<#Type#>]?\n'
        elif isinstance(value,dict):
            encodeDict(value,key)
            modelStr += '    var : <#Type#>?\n'
        elif isinstance(value, int):
            modelStr += '    var ' + strKey + ' = 0\n'
            keyTypes.append({strKey: 'Int'})
            keyIfIndexDic[strKey] = '0'
        elif isinstance(value, bool):
            modelStr += '    var ' + strKey + ' = false\n'
            keyTypes.append({strKey: 'Bool'})
            keyIfIndexDic[strKey] = '0'
        elif isinstance(value, float):
            modelStr += '    var ' + strKey + ': CGFloat = 0\n'
            keyTypes.append({strKey: 'CGFloat'})
            keyIfIndexDic[strKey] = '0'
        elif isinstance(value, str):
            modelStr += '    var ' + strKey + ': String?\n'
            keyTypes.append({strKey: 'String'})
            keyIfIndexDic[strKey] = '1'
        else:
            modelStr += '    var ' + strKey + ': <#Type#>\n'
            keyTypes.append({strKey: '<#Type#>'})


    if caseLock:
        modelStr += '\n    enum CodingKeys: String, CodingKey{\n'
        for item in keyTypes:
            for itemKey in item.keys():
                modelStr += '        case ' + itemKey + '\n'
                break
        modelStr += '    }\n'

    modelStr += '\n'
    if requiredLok:
        modelStr += '    required init(from decoder: Decoder) throws{\n'
        modelStr += '        let container = try decoder.container(keyedBy: CodingKeys.self)\n'
        for item in keyTypes:
            for itemKey in item.keys():
                if keyIfIndexDic[itemKey] == '0':
                    modelStr += '        if let value = try container.decodeIfPresent(' + item[itemKey] + '.self, forKey: .' + itemKey + '){\n'
                    modelStr += '            ' + itemKey + ' = value\n'
                    modelStr += '            }\n'
                else:
                    modelStr += '        ' + itemKey + ' = try container.decodeIfPresent(' + item[itemKey] + '.self, forKey: .' + itemKey + ')\n'
                break
        modelStr += '    }\n'


def saveModelStr():
    print(modelStr)
    f = open('/Users/user/Desktop/PythonDemo/CreateSwiftClass/NGSwiftJsonModel','w')
    f.write(modelStr)
    f.close()

if __name__ == '__main__':
    startWord()
    saveModelStr()
