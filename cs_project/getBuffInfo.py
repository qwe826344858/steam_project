import json
import random
import time

import requests


category_group = ['knife']

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# 饰品类型
item_type = ['knife']


def getBuffInfo():
    ret, pageInfo = getItemTotal()
    if not ret:
        return False

    print(pageInfo)
    page = 1
    page_size = 500

    # 请求获取数据
    while 1:
        url = f"https://buff.163.com/api/market/sell_order/top_bookmarked"
        response = requests.get(url, params=_apiInput(page,page_size), cookies=_getCookie(), headers=_getHeaders(), proxies=proxies)
        if response.status_code != 200:
            print(f"getBuffInfo 请求失败 {response.status_code}")
            return False

        data = json.loads(response.content)


        if data['data']['total_page'] <= page:
            break
        else:
            page += 1
            # 随机下模拟时间
            time.sleep(random.random())



    # file = open("buff_cs_item.txt", "w")
    # file.write(json.dumps(json_data))
    # file.close()


def getItemTotal():
    url = f"https://buff.163.com/api/market/sell_order/top_bookmarked"
    response = requests.get(url, params=_apiInput(), cookies=_getCookie(), headers=_getHeaders(), proxies=proxies)
    if response.status_code != 200:
        print(f"getItemTotal 请求失败 {response.status_code}")
        return False, {}

    data = json.loads(response.content)
    ret = {
        'total_count': data['data']['total_count'],
        'total_page': data['data']['total_page'],
    }

    return True, ret


def _getHeaders():
    headers = {
        'authority': 'buff.163.com',
        'accept': 'application/json, text/javascript, */*; q=0.01',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'no-cache',
        # Requests sorts cookies= alphabetically
        # 'cookie': 'P_INFO=18907742278|1679544091|1|netease_buff|00&99|null&null&null#gud&440300#10#0|&0||18907742278; Device-Id=s4N5C0ScKHcwXeEPqWbg; Locale-Supported=zh-Hans; game=csgo; remember_me=U1094246188|wNCHnSpCUJk3WLvEnSWyl4pJqgJo7TPU; session=1-SaXyNMgDBX7Mn-ph9Mu5Tp3ADDsv-McHJfg8pHbbRC2G2046181492; csrf_token=ImQyMWRmZGFlM2JlZTUzNmI0Y2RjZDQ0ODg0OTA4MjliYTcxYzNlY2Ui.GNmOXQ.WD2l80DK3bTyEzWfinJT-1rXgM4',
        'dnt': '1',
        'pragma': 'no-cache',
        'referer': 'https://buff.163.com/market/csgo',
        'sec-ch-ua': '"Chromium";v="122", "Not(A:Brand";v="24", "Microsoft Edge";v="122"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
        'x-requested-with': 'XMLHttpRequest',
    }

    return headers


def _getCookie():
    cookies = {
        'P_INFO': '18907742278|1679544091|1|netease_buff|00&99|null&null&null#gud&440300#10#0|&0||18907742278',
        'Device-Id': 's4N5C0ScKHcwXeEPqWbg',
        'Locale-Supported': 'zh-Hans',
        'game': 'csgo',
        'remember_me': 'U1094246188|wNCHnSpCUJk3WLvEnSWyl4pJqgJo7TPU',
        'session': '1-SaXyNMgDBX7Mn-ph9Mu5Tp3ADDsv-McHJfg8pHbbRC2G2046181492',
        'csrf_token': 'ImQyMWRmZGFlM2JlZTUzNmI0Y2RjZDQ0ODg0OTA4MjliYTcxYzNlY2Ui.GNmOXQ.WD2l80DK3bTyEzWfinJT-1rXgM4',
    }
    return cookies


def _apiInput(page_num=1, page_size=20, category_group='knife'):
    params = {
        'game': 'csgo',
        'page_num': page_num,
        'page_size': page_size,
        'category_group': category_group,
        'tab': 'selling',
        '_': '1710750906681',
    }
    return params


if __name__ == '__main__':
    getBuffInfo()
