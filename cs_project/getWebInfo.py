import json
import random
import time

import requests
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from bs4 import BeautifulSoup

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

mapCurrency = {
    "1": "USD"
}

# 被拉进小黑屋力 迟点再请求重试吧
retry_sleep_time = 120

def funcStart():
    url = "https://gateway.inshealth.cc/api/insUnderwriting/multiplayer/searchDiseaseModuleList?deptCode=8888"
    data = {"operateNumber": "20246597aac1e4b01d08bcb2377c"}  # 替换成你要发送的数据
    pubKey = b"bgD11G&Ix@XUC1vc"

    js = json.dumps(data)
    byte_data = js.encode("utf-8")  # 将Unicode字符串编码为字节对象

    req = _trans(byte_data, pubKey, 1)
    response = requests.post(url, req)
    resp = _trans(response.content, pubKey, 2)

    print(resp.decode("utf-8"))  # 输出返回结果


def funcGetSteamInfo():
    total_count = 0  # 总和计数
    retry_count = 0  # 重试次数
    ret, total_count = _getCSItemTotal()
    if not ret:
        return False

    index = 0
    json_data = {}
    while True:
        url = f"https://steamcommunity.com/market/search/render/?query=&start={index}&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730"
        if index >= total_count:
            break
        else:
            index += 100
            print(f"index:{index}")
            time.sleep(random.uniform(1.1, 5.5))

        req = {}
        try:
            response = requests.post(url, req, headers=_getHeaders(), proxies=proxies)
            if response.status_code != 200:
                print(f"请求被拦截了,延迟{retry_sleep_time}秒再重试下 index:{index}")
                time.sleep(retry_sleep_time)
                if retry_count > 5:
                    print(f"重试次数超过5次,关闭程序 count:{retry_count}")
                    break
                index -= 100
                retry_count += 1
                continue
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            index -= 100
            retry_count += 1
            continue
        else :
            if retry_count > 0:
                print(f"清空重试次数 count:{retry_count}")
                retry_count = 0

        element = json.loads(response.content)
        data = init_data(element["results_html"])
        if data == None:
            break
        # print(element["results_html"])

        json_data.update(html_to_json(data))

    file = open("/home/lighthouse/test_py/cs_project/log.txt", "w",encoding='utf-8')
    file.write(json.dumps([json_data],ensure_ascii=False))
    file.close()


def _getCSItemTotal():
    url = "https://steamcommunity.com/market/search/render/?query=&start=10&count=100&search_descriptions=0&sort_column=popular&sort_dir=desc&appid=730"
    req = {}
    response = requests.post(url, req, headers=_getHeaders(), proxies=proxies)
    element = json.loads(response.content)
    print(element)
    if element == None:
        print("element is None")
        return False, 0

    if element['success'] != True:
        print("_getCSItemTotal try connect faild!")
        return False, 0

    total_count = element['total_count']
    return True, total_count


# AES加密
def encrypt(data, pubKey):
    cipher = Cipher(algorithms.AES(pubKey), modes.ECB(), default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data) + encryptor.finalize()
    return base64.b64encode(encrypted_data)


# AES解密
def decrypt(data, pubKey):
    decoded_data = base64.b64decode(data)
    cipher = Cipher(algorithms.AES(pubKey), modes.ECB(), default_backend())
    decryptor = cipher.decryptor()
    return decryptor.update(decoded_data) + decryptor.finalize()


# 格式化数据
def init_data(data):
    dir = {'\n': "", '\t': "", '\r': ""}
    return data.translate(str.maketrans(dir))


# 数据格式转换下 再加解密
def _trans(byte_data, pubKey, type=1):
    if type == 1:
        obj = padding.PKCS7(128).padder()
        data = obj.update(byte_data) + obj.finalize()
        return encrypt(data, pubKey)
    elif type == 2:
        data = decrypt(byte_data, pubKey)
        unpadder = padding.PKCS7(128).unpadder()
        return unpadder.update(data) + unpadder.finalize()


# 递归函数，将HTML元素转换为JSON格式
def html_to_json(element):
    # soup = BeautifulSoup(element, "html.parser")
    # # 提取所有的<span>元素
    # span_elements = soup.find_all('span')
    #
    # # 打印所有的<span>元素文本内容
    # for span in span_elements:
    #     if span.text.strip() == "":
    #         continue
    #     else:
    #         print(span.text.strip())
    #         #break

    getData = {}
    soup = BeautifulSoup(element, "lxml")
    arr = soup.select(".market_listing_row_link")
    for info_1 in arr:
        level_Name = info_1.div
        nameInfo = level_Name.attrs

        # 在售数量
        sale_online_count_Info = level_Name.select(".market_listing_price_listings_block")
        sale_online_count = sale_online_count_Info[0].div.span.span.attrs['data-qty']

        # 获取售价和货币类型
        sale_price_Info = level_Name.select(".market_listing_their_price")
        sale_price_next = sale_price_Info[0].select(".normal_price")
        show_sale_prices = sale_price_next[0].select(".normal_price")[0].text
        sale_price = sale_price_next[0].select(".normal_price")[0].attrs['data-price']
        sale_currency = mapCurrency[sale_price_next[0].select(".normal_price")[0].attrs['data-currency']]


        # 获取中文名称
        item_name_block_info = level_Name.select(".market_listing_item_name_block")
        item_name_block_span = item_name_block_info[0].select(".market_listing_item_name")
        item_cn_name = item_name_block_span[0].text


        getData[nameInfo['data-hash-name']] = {
            'item_cn_name':item_cn_name,
            'sell_online_count': sale_online_count,
            'pic_url': "",
            'show_prices': show_sale_prices,
            'prices': sale_price,
            'currency': sale_currency
        }

    print(json.dumps(getData))
    return getData


# 获取请求头
def _getHeaders():
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Cookie": "sessionid=f559f7a00dc64873037929d8; timezoneOffset=28800,0; recentlyVisitedAppHubs=730; app_impressions=730@2_9_100000_; strInventoryLastContext=730_2; strResponsiveViewPrefs=touch; steamCountry=HK%7Cb9dd509e17a75761969f33432dcdf5f2",
        "Host": "steamcommunity.com",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "User-Agent": "'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'",
        "sec-ch-ua": 'Not_A Brand";v="8", "Chromium";v="120", "Microsoft Edge";v="120"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows"
    }
    return headers


# 设置cookie
def _getCookie():
    cookie = "sessionid=f559f7a00dc64873037929d8; timezoneOffset=28800,0; recentlyVisitedAppHubs=730; app_impressions=730@2_9_100000_; strInventoryLastContext=730_2; strResponsiveViewPrefs=touch; steamCountry=HK%7Cb9dd509e17a75761969f33432dcdf5f2"
    return cookie


if __name__ == '__main__':
    funcGetSteamInfo()
