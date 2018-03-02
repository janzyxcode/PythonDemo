# _*_ coding: utf-8 _*_

import json

caseLock = False
requiredLok = True


modelStr = ''

def startWord():
    with open('/Users/user/Desktop/Python Tool/NGSwiftJson','r',encoding='utf-8') as file_obj:
        data = json.load(file_obj)
        # print(json.dumps(data,indent=4,ensure_ascii=False))
        print('\n-----Encoding....')
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
    global  modelStr
    modelStr += '\n' + str(dicKey) + 'Model：\n'
    keyTypes = []
    for key in dic.keys():
        value = dic[key]
        # print('key: ' + str(key) + '：' + str(type(value)) + '   ' + str(value))
        if isinstance(value,list):
            encodeJson(value,str(key))
            modelStr += '    var : [<#Type#>]?\n'
        elif isinstance(value,dict):
            encodeDict(value,key)
            modelStr += '    var : <#Type#>?\n'
        elif isinstance(value, int):
            modelStr += '    var ' + str(key) + ' = 0\n'
            keyTypes.append({str(key): 'Int'})
        elif isinstance(value, bool):
            modelStr += '    var ' + str(key) + ' = false\n'
            keyTypes.append({str(key): 'Bool'})
        elif isinstance(value, float):
            modelStr += '    var ' + str(key) + ': CGFloat = 0\n'
            keyTypes.append({str(key): ' CGFloat'})
        elif isinstance(value, str):
            modelStr += '    var ' + str(key) + ': String?\n'
            keyTypes.append({str(key): 'String'})
        else:
            modelStr += '    var ' + str(key) + ': <#Type#>\n'
            keyTypes.append({str(key): '<#Type#>'})


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
                modelStr += '        if let value = try container.decodeIfPresent(' + item[
                    itemKey] + '.self, forKey: .' + itemKey + '){\n'
                modelStr += '            ' + itemKey + ' = value\n'
                modelStr += '            }\n'
                break
        modelStr += '    }\n'
    modelStr += '\n\n\n'


def saveModelStr():
    print(modelStr)
    f = open('/Users/user/Desktop/Python Tool/NGSwiftJsonModel','w')
    f.write(modelStr)
    f.close()

if __name__ == '__main__':
    startWord()
    saveModelStr()
