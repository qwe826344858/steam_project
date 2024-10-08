import json
import sys

import requests
import os
import inspect

errInfo = {
    "ERR_REQUEST":{
        "errCode": 10001,
        "errMsg": "请求失败",
    }
}

def _cUrlTrans(cUrl_bash, lang='python'):
    pyCode = ''
    req = {
        'code': cUrl_bash,
        'lang': lang
    }
    response = requests.post("https://www.lddgo.net/api/CurlGenerateCode", json=req)
    element = json.loads(response.content)
    print(element)
    return pyCode


def setReturn(errCode=0, errMsg='success', data={}):
    return {
        "errCode": errCode,
        "errMsg": errMsg,
        "data": data,
    }

# 传值为空时 根据类型赋值默认值
def initSet(variable,type = "str"):
    try:
        variable
    except NameError:
        if type == "str":
            return ""
        elif type == "num":
            return 0
        elif type == "arr":
            return []
        elif type == "obj":
            return {}
    else:
        return variable


# 获取调用方的文件路径
def getCurrentFileInfo():
    frame = inspect.currentframe().f_back
    file_info = inspect.getframeinfo(frame)
    file_name = file_info.filename
    file_path = os.path.abspath(file_name)
    return file_name, file_path

# 获取调用方的函数名称
def getCurrentMethodName():
    frame = inspect.currentframe().f_back
    method_name = frame.f_code.co_name
    return method_name


def runDaemon(api):
    # 通过命令行输入方法名进行调用
    method_name = sys.argv[1]     # 获取命令中第一个额外参数

    # 获取方法对象
    method = getattr(api, method_name, None)

    # 检查方法是否存在
    if method is None or not callable(method):
        print(f"方法 '{method_name}' 不存在或不可调用")
        sys.exit(1)

    # 调用方法
    method()


def array_column(arr, col):
    retList = []
    for item in arr:
        retList.append(item.get(col))
    return retList


# 根据系统的核心数量获取尽可能多可创建的线程数量
def GetThreadCountByCore() -> int:
    cnt = os.cpu_count()
    if not cnt or cnt == 1:
        return 2

    return cnt * 2 - 1


# cUrl(bash) 转 对应语言的代码
if __name__ == '__main__':
    str = "curl 'https://buff.163.com/api/market/sell_order/top_bookmarked?game=csgo&page_num=1&category_group=knife&tab=top-bookmarked&_=1710750906681' \
  -H 'authority: buff.163.com' \
  -H 'accept: application/json, text/javascript, */*; q=0.01' \
  -H 'accept-language: zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6' \
  -H 'cache-control: no-cache' \
  -H 'cookie: P_INFO=18907742278|1679544091|1|netease_buff|00&99|null&null&null#gud&440300#10#0|&0||18907742278; Device-Id=s4N5C0ScKHcwXeEPqWbg; Locale-Supported=zh-Hans; game=csgo; remember_me=U1094246188|wNCHnSpCUJk3WLvEnSWyl4pJqgJo7TPU; session=1-SaXyNMgDBX7Mn-ph9Mu5Tp3ADDsv-McHJfg8pHbbRC2G2046181492; csrf_token=ImQyMWRmZGFlM2JlZTUzNmI0Y2RjZDQ0ODg0OTA4MjliYTcxYzNlY2Ui.GNmOXQ.WD2l80DK3bTyEzWfinJT-1rXgM4' \
  -H 'dnt: 1' \
  -H 'pragma: no-cache' \
  -H 'referer: https://buff.163.com/market/csgo' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-site: same-origin' \
  -H 'user-agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0' \
  -H 'x-requested-with: XMLHttpRequest'"
    _cUrlTrans(str, 'go')
