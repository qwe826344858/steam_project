import json

import requests

def test():
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'apptype': '1',
        'authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmOWYwYzFjYTIzMWI0YTI2OGVjMDNlNTUwN2RjNjA0YiIsIm5hbWVpZCI6IjY3OTg2MTIiLCJJZCI6IjY3OTg2MTIiLCJ1bmlxdWVfbmFtZSI6IllQMDAwNjc5ODYxMiIsIk5hbWUiOiJZUDAwMDY3OTg2MTIiLCJ2ZXJzaW9uIjoiaGNtIiwibmJmIjoxNzIxMDQwMTE0LCJleHAiOjE3MjE5MDQxMTQsImlzcyI6InlvdXBpbjg5OC5jb20iLCJhdWQiOiJ1c2VyIn0.ZuXSA3F7O8kNUj51CLnwi7GAMSYMcj5MP3zc4E8eY4I',
        'cache-control': 'no-cache',
        # Already added when you pass json=
        # 'content-type': 'application/json',
        'd': 'p=p&b=u&v=1',
        'dnt': '1',
        'origin': 'https://www.youpin898.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://www.youpin898.com/',
        'sec-ch-ua': '"Microsoft Edge";v="125", "Chromium";v="125", "Not.A/Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'uk': '5AC0hw0srckEA2vmykxMF3wVqSVZlAN9GCwW8Qp38zqAvLGcLSWOM2IjDPZjekH1L',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 Edg/125.0.0.0',
    }

    pageIndex = 1
    countAmount = 0
    while 1:
        json_data = {
            'orderStatus': 0,
            'pageIndex': pageIndex,
            'pageSize': 10,
            'keys': '',
        }

        response = requests.post('https://api.youpin898.com/api/youpin/bff/order/pc/rent-out-record-list', headers=headers,
                                 json=json_data)

        if response.status_code != 200:
            print("请求失败!")
            return

        data = json.loads(response.content)['data']
        if not data["orderList"]:
            print("所有数据已收集")
            break

        #print(f"data:",data["orderList"])
        for val in data["orderList"]:
            print(val['orderInfo']['totalAmount'])
            countAmount += val['orderInfo']['totalAmount']

        pageIndex += 1


    print(f"总收益:{countAmount/100}")
    print(f"预计到手:{countAmount / 100 * 0.75}")

    return


if __name__ == '__main__':
    test()