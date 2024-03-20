import json
import requests


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


