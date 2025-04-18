import datetime
import json
import re
import threading
import time
from datetime import timedelta
import concurrent.futures
from matplotlib import font_manager

from common_tools.redisHelper import get_redis_connection, getRedisString, setRedisString
from common_tools.tools import runDaemon
from common_tools.loggerHelper import Logger
from DAO import cs_item_dao

# 初始化日志
Logger.init()

mapInfo = []    # 商品信息,全局变量
max_day = 30    # 查询的商品价格时间维度周期
max_Image_output = 500 # 单次执行最大导出走势图数量

picLock = threading.Lock()
class VisualGraphics:
    dao = None


    def __init__(self):
        self.dao = cs_item_dao.ItemDao()

    def testlog(self):
        Logger.info("新增测试")

    def GetVisualGraphics(self):

        redis_conn = get_redis_connection()
        key = f"VISUAL_GRAPHICS_LAST_ITEM_ID_" + datetime.datetime.now().strftime("%Y%m%d")
        ret,lastID = getRedisString(key)
        if lastID is None or ret is False:
            lastID = 0
            setRedisString(key, lastID, 86400)

        lastID = int(lastID)
        global mapInfo
        ret,idList,mapInfo = self.getItemIdList(lastID)
        if not ret :
            Logger.info("获取商品信息失败!")
            return

        if not idList:
            Logger.info(f"已导出所有商品走势图 lastID:{lastID}")
            return

        # 查询每日且生成走势图
        ret = self.transItemInfo2Pic(idList,lastID)
        if not ret:
            Logger.info(f"生成走势图失败!idList:{idList}")
            return

        Logger.info("流程结束!")
        return


    def transItemInfo2Pic(self,param,lastItemID):
        Logger.info(f"px:{param} lastItemID:{lastItemID}")
        cnt = 0
        # 使用日价表 取30天的价格走势
        current_time = datetime.datetime.now()
        end = int(current_time.strftime('%Y%m%d'))
        begin = int((current_time - timedelta(days=max_day)).strftime('%Y%m%d'))
        self.dao.SetTable(self.dao.TABLE_ITEM_SINGLE_DAY)
        #with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        for item_id in param:
            self.getSingleItemInfo2trans(item_id,begin,end)
            cnt += 1
            if cnt >= max_Image_output:
                Logger.info(f"达到单次导出走势图上限! cnt:{cnt} lastItemID:{lastItemID}")
                break

        return True

    def getSingleItemInfo2trans(self,item_id,begin,end):
        arr = []
        lastID = 0
        while True:
            ret,dataList = self.dao.getIteamInfoSingleDayByLastID(filter={'item_id':item_id},lastID=lastID,pageSize=1000,begin=begin,end=end)
            if not ret:
                Logger.info(f"查询失败!id:{item_id}")
                return False
            if not dataList:
                Logger.info(f"查询为空!结束查询 ==> id:{item_id}")
                break

            Logger.info(f"single day datalist:"+json.dumps(dataList))
            for data in dataList:
                arr.append({
                    "calc_day":data.get('calc_day',0),
                    "sell_online_count":data.get('sell_online_count',0),
                    "prices":data.get('prices',0)
                })
            lastID = dataList[-1].get('id')

        if arr:
            Logger.info(f"=====>输出图片 item:{item_id}")
            self.ItemInfo2VisualGraphics(arr, f"{item_id}_{mapInfo[item_id]}")
            redis_conn = get_redis_connection()
            key = f"VISUAL_GRAPHICS_LAST_ITEM_ID_" + datetime.datetime.now().strftime("%Y%m%d")
            setRedisString(key, item_id, 86400)


        return True


    def getItemIdList(self,lastID = 0):

        idList = []
        mapInfo = {}
        while True:
            ret, dataList = self.dao.getIteamInfoByLastID(lastID, 500, "`Fid`")
            if not ret:
                Logger.info("getIteamInfoByLastID 查询失败! 结束返回")
                return False, [] ,{}

            if len(dataList) == 0:
                break

            lastID = dataList[-1].get('id')
            Logger.info(f"lastID:{lastID}")
            for v in dataList:
                item_id = v.get("id", '')
                item_cn_name = v.get("item_cn_name","")
                idList.append(item_id)
                mapInfo[item_id] = item_cn_name



        return True, idList,mapInfo

    def ItemInfo2VisualGraphics(self, data, file_name):
        if not data:
          Logger.info(f"无数据,不生成走势图! file_name:{file_name}")
          return True

        # Logger.info(f"VisualGraphics input data:"+json.dumps(data))

        # 数据示例
        # data = [
        #     {"date": "2023-08-01", "quantity": 100, "selling_price": 20.5},
        #     {"date": "2023-08-02", "quantity": 150, "selling_price": 19.0},
        #     {"date": "2023-08-03", "quantity": 120, "selling_price": 21.5},
        #     # ...（更多数据）
        # ]

        # 使用GUI 的后端，在本地显示图形 服务器上就linux就不用了
        # matplotlib.use('TKAgg')

        # # # 设置字体为支持中文的字体
        # # windows
        # matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
        # matplotlib.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

        import matplotlib
        matplotlib.use('Agg')
        import seaborn as sns
        import pandas as pd
        import matplotlib.pyplot as plt
        # # linux
        # 设置字体路径
        font_path = '/usr/share/fonts/python_font/SimHei.ttf'  # 根据实际路径调整
        font_prop = font_manager.FontProperties(fname=font_path)
        plt.rcParams['font.family'] = font_prop.get_name()

        # 将数据转换为 DataFrame
        df = pd.DataFrame(data)

        # 确保日期列为 datetime 类型
        df['date'] = pd.to_datetime(df['calc_day'],format='%Y%m%d')
        df['sell_online_count'] = pd.to_numeric(df['sell_online_count'])
        df['prices'] = pd.to_numeric(df['prices'])

        # 设置日期为索引
        df.set_index('date', inplace=True)

        # 选择最近 30 天的数据
        end_date = df.index.max()
        start_date = end_date - timedelta(days=len(data))
        recent_data = df[start_date:end_date]
        # Logger.info(f"recent_data:{recent_data}")

        # 可视化
        plt.figure(figsize=(12, 6))

        # 绘制在售数量
        plt.subplot(2, 1, 1)
        sns.lineplot(data=recent_data, x='date', y='sell_online_count', marker='o', label='在售数量')
        #sns.lineplot(data=recent_data, x='date', y='sell_online_count', marker='o')
        plt.title('在售数量随时间变化')
        plt.xlabel('日期')
        plt.ylabel('在售数量')
        plt.xticks(rotation=45)

        # 绘制售价
        plt.subplot(2, 1, 2)
        #sns.lineplot(data=recent_data, x='date', y='selling_price', marker='o', color='orange')
        sns.lineplot(data=recent_data, x=recent_data.index, y='prices', marker='o', color='orange', label='售价')
        plt.title('售价随时间变化')
        plt.xlabel('日期')
        plt.ylabel('售价')
        plt.xticks(rotation=45)

        plt.tight_layout()

        # 保存图形为图片
        file_name = re.sub(r"[^\u4e00-\u9fa5A-Za-z0-9]+", "_", file_name)
        save_name = f"/home/lighthouse/test_py/Visualization/{file_name}.png"
        #Logger.info(f"save_name:{save_name}")


        plt.savefig(save_name)
        time.sleep(1)
        # 显示图形 服务器上就linux就不用了
        # plt.show()
        plt.close()



        Logger.info(f"file_name:{file_name} 走势图导出成功!")
        return True

    def test(self):
        data = [
            {"calc_day": "2023-08-01", "sell_online_count": 100, "prices": 20.5},
            {"calc_day": "2023-08-02", "sell_online_count": 150, "prices": 19.0},
            {"calc_day": "2023-08-03", "sell_online_count": 120, "prices": 21.5},
            {"calc_day": "2023-08-04", "sell_online_count": 100, "prices": 20.5},
            {"calc_day": "2023-08-05", "sell_online_count": 150, "prices": 19.0},
            {"calc_day": "2023-08-06", "sell_online_count": 120, "prices": 21.5},
            {"calc_day": "2023-08-07", "sell_online_count": 100, "prices": 20.5},
            {"calc_day": "2023-08-08", "sell_online_count": 150, "prices": 19.0},
            {"calc_day": "2023-08-09", "sell_online_count": 120, "prices": 21.5},
            {"calc_day": "2023-08-10", "sell_online_count": 100, "prices": 20.5},
            {"calc_day": "2023-08-11", "sell_online_count": 150, "prices": 19.0},
            {"calc_day": "2023-08-12", "sell_online_count": 120, "prices": 21.5},
            {"calc_day": "2023-08-13", "sell_online_count": 100, "prices": 20.5},
            {"calc_day": "2023-08-14", "sell_online_count": 150, "prices": 19.0},
            {"calc_day": "2023-08-15", "sell_online_count": 120, "prices": 21.5},
            # ...（更多数据）
        ]

        # file_name = "test2Image"
        # self.ItemInfo2VisualGraphics(data=data, file_name=file_name)
        idList= [i for i in range(1,11)]
        global mapInfo
        mapInfo = {i:i for i in range(1, 11)}
        self.transItemInfo2Pic(idList,0)

if __name__ == '__main__':
    runDaemon(api=VisualGraphics())
