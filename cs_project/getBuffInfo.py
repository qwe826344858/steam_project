import json
import random
import time

import requests
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.redisHelper import get_redis_connection, release_redis_connection, setRedisHash
from common_tools.tools import setReturn, errInfo

proxies = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890",
}

# 饰品类型
item_type_list = ['knife','hands','rifle','pistol','smg','shotgun','machinegun','sticker','type_customplayer']  #'other'   暂不支持格式
# 最大重试次数
max_retry = 5

# TODO session  怎么去请求服务器刷新呢？
session = '1-yiQ3v2F83rZmKoWBTjkbq9rS474updPTm6NegCEv4XY72046181492'

# 取buff信息
def getBuffInfo():
    for item_type in item_type_list:
        page = 1
        page_size = 500
        retry_count = 0
        all_data = {}

        # 请求获取数据
        while 1:
            # url = f"https://buff.163.com/api/market/sell_order/top_bookmarked"
            # sell_type = "top_bookmarked"
            url = "https://buff.163.com/api/market/goods"
            sell_type = "goods"
            response = requests.get(url, params=_apiInput(page, page_size,category_group=item_type), cookies=_getCookie(), headers=_getHeaders(),
                                    proxies=proxies)
            if response.status_code != 200:
                if retry_count > max_retry:
                    print(f"getBuffInfo 请求失败 {response.status_code} retry_count:{retry_count} response:{response.content}")
                    return setReturn(errcode=errInfo['ERR_REQUEST']['errCode'], errMsg=errInfo['ERR_REQUEST']['errMsg'],data={})
                else:
                    print(f"getBuffInfo 重试第{retry_count}次 5秒后重试")
                    time.sleep(5)
                    retry_count += 1
                    continue
            else:
                if retry_count > 0:
                    print("请求成功! 重试次数 清0")
                    retry_count = 0

            data = json.loads(response.content)
            all_data.update(_tranLocalData(data, sell_type))

            if data['data']['total_page'] <= page:
                print(f"已获取全部数据! total_page:{data['data']['total_page']} current_page:{page}")
                break
            else:
                page += 1
                # 随机下请求时间 模拟人为操作
                # TODO 动态切换代理ip
                sleep_time = random.random()
                print(f"item_type:{item_type} sleep_time:{sleep_time} page:{page}")
                time.sleep(sleep_time)

        saveInfo2RDS(all_data,item_type)
        item_count = len(all_data)
        file_data = {
            "data": all_data,
            "itme_count": item_count
        }

        # 释放掉占用的内存
        all_data = []
        file = open(f"buff_cs_item_{item_type}.txt", "w", encoding='utf-8')
        file.write(json.dumps(file_data, ensure_ascii=False))
        file.close()


def _transGoodsInfos_top(rawGoodsInfos):
    retData = {}
    for k, v in rawGoodsInfos.items():
        retData[k] = {
            "appid": v['appid'],
            "goods_id": v['goods_id'],
            "icon_url": v['icon_url'],  # 饰品图片
            "market_hash_name": v['market_hash_name'],  # steam名称
            "name": v['name'],  # 中文名称
            "steam_price_cny": v['steam_price_cny'],  # steam 人民币售价
            "tags": v['tags'],
        }

    return retData


def _transItemsInfos_top(goodsInfos, rawItems):
    retData = {}
    for v in rawItems:
        singleGoods = goodsInfos[f"{v['goods_id']}"]
        retData[v['goods_id']] = {
            "price": v['price'],  # buff售价
            "icon_url": singleGoods['icon_url'],  # 饰品图片
            "market_hash_name": singleGoods['market_hash_name'],  # steam名称
            "name": singleGoods['name'],  # 中文名称
            "steam_price_cny": singleGoods['steam_price_cny'],  # steam 人民币售价
            "paintindex": v['asset_info']['info']['paintindex'],  # 皮肤编号
            "paintseed": v['asset_info']['info']['paintseed'],  # 图案模板
            "paintwear": v['asset_info']['paintwear'],  # 具体磨损数值
            "exterior": {  # 磨损昵称
                "internal_name": singleGoods['tags']['exterior']['internal_name'],
                "localized_name": singleGoods['tags']['exterior']['localized_name'],
            },
            "quality": {  # 是否 StatTrak™
                "internal_name": singleGoods['tags']['quality']['internal_name'],
                "localized_name": singleGoods['tags']['quality']['localized_name'],
            },
            "rarity": {  # 品质等级
                "internal_name": singleGoods['tags']['rarity']['internal_name'],
                "localized_name": singleGoods['tags']['rarity']['localized_name'],
            }
        }

        if v['asset_info']['info'].get('phase_data') is not None:
            retData[v['goods_id']]['phase_data'] = v['asset_info']['info']['phase_data']

    return retData


def _transIteasInfos_common(rawItems):
    retData = {}
    for v in rawItems:
        retData[v['id']] = {
            "sell_min_price": v['sell_min_price'],  # buff最低售价
            "icon_url": v['goods_info']['icon_url'],  # 饰品图片
            "market_hash_name": v['market_hash_name'],  # steam名称
            "name": v['name'],  # 中文名称
            "steam_price_cny": v['goods_info']['steam_price_cny'],  # steam 人民币售价
            # "paintindex": v['asset_info']['info']['paintindex'],  # 皮肤编号
            # "paintseed": v['asset_info']['info']['paintseed'],  # 图案模板
            # "paintwear": v['asset_info']['paintwear'],  # 具体磨损数值
        }

        try:
            retData[v['id']]["exterior"] = {  # 磨损昵称
                "internal_name": v['goods_info']['info']['tags']['exterior']['internal_name'],
                "localized_name": v['goods_info']['info']['tags']['exterior']['localized_name'],
            }
            retData[v['id']]["quality"] = {  # 是否 StatTrak™
                "internal_name": v['goods_info']['info']['tags']['quality']['internal_name'],
                "localized_name": v['goods_info']['info']['tags']['quality']['localized_name'],
            }
            retData[v['id']]["rarity"] = {  # 品质等级
                "internal_name": v['goods_info']['info']['tags']['rarity']['internal_name'],
                "localized_name": v['goods_info']['info']['tags']['rarity']['localized_name'],
            }
        except:
            continue

    return retData


# 转出本地使用的数据
def _tranLocalData(data, sell_type):
    if sell_type == "top_bookmarked":  # 热门饰品
        rawGoodsInfos = data['data']['goods_infos']
        rawItems = data['data']['items']
        return _transItemsInfos_top(_transGoodsInfos_top(rawGoodsInfos), rawItems)
    elif sell_type == "goods":
        rawItems = data['data']['items']
        return _transIteasInfos_common(rawItems)


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
        'session': session,
        'csrf_token': 'ImQyMWRmZGFlM2JlZTUzNmI0Y2RjZDQ0ODg0OTA4MjliYTcxYzNlY2Ui.GNmOXQ.WD2l80DK3bTyEzWfinJT-1rXgM4',
    }

    # 'remember_me': 'U1094246188|C2eJpHmMuyBZlfsKgadBkbnkq3j8xtEd',
    # 'session': '1-_WCb5E-Z6GiXSZ4qY7_SREQ6epqxnSPiSZr2ux2FGYWO2046181492',
    # 'csrf_token': 'IjAxZjcwNmFkN2ViNjRlOGU1N2RhM2JkMWY2NTczODk5MmM3NTcwNDMi.GOQCxg.7kEtNBT_SR20Xvh0q3IwmSXLRxQ',
    return cookies


def _apiInput(page_num=1, page_size=20, category_group='knife'):
    params = {
        'game': 'csgo',
        'page_num': page_num,
        'page_size': page_size,
        'category_group': category_group,
        'tab': 'selling',
        '_': '1710750906681',
        'sort_by': 'price.desc',        # 按价格倒叙排序
    }
    return params


def saveInfo2RDS(data,name):
    #data 是纯object类型 所以取的时候取items()
    redis_conn = get_redis_connection()
    for k, val in data.items():
        key = f"{name}_{k}"
        setRedisHash(name,key,val,0)
    release_redis_connection(redis_conn)
    return True


if __name__ == '__main__':
    getBuffInfo()
