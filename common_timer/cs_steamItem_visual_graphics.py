import threading
from datetime import timedelta
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from common_tools.tools import runDaemon, array_column
from common_tools.loggerHelper import Logger
from DAO import cs_item_dao

# 初始化日志
Logger.init()


class VisualGraphics:
    dao = None


    def __init__(self):
        self.dao = cs_item_dao.ItemDao()

    def testlog(self):
        Logger.info("新增测试")

    def GetVisualGraphics(self):
        ret,idList,mapInfo = self.getItemIdList()
        if not ret :
            Logger.info("获取商品信息失败!")
            return

        # 切割id列表为多个线程执行
        thread_list = []
        index = (len(idList)-1)//2
        paramList = [idList[index:],idList[:index]]
        for param in paramList:
            th = threading.Thread(target=self.transItemInfo2Pic(param))
            thread_list.append(th)
            th.start()


        for th in thread_list:
            th.join()

        return


    def transItemInfo2Pic(self,param):
        begin = 0
        end = 500
        max = len(param) - 1
        while 1:
            if end >= max:
                break
            idList = param[begin:end]



            begin = end
            end += 500




    def getItemIdList(self):

        lastID = 0
        idList = []
        mapInfo = {}
        while 1:
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
        # 将数据转换为 DataFrame
        df = pd.DataFrame(data)

        # 确保日期列为 datetime 类型
        df['date'] = pd.to_datetime(df['calc_day'])

        # 设置日期为索引
        df.set_index('date', inplace=True)

        # 选择最近 30 天的数据
        end_date = df.index.max()
        start_date = end_date - timedelta(days=30)
        recent_data = df[start_date:end_date]

        # 可视化
        plt.figure(figsize=(12, 6))

        # 绘制在售数量
        plt.subplot(2, 1, 1)
        sns.lineplot(data=recent_data, x=recent_data.index, y='sell_online_count', marker='o')
        plt.title('在售数量随时间变化')
        plt.xlabel('日期')
        plt.ylabel('在售数量')
        plt.xticks(rotation=45)

        # 绘制售价
        plt.subplot(2, 1, 2)
        sns.lineplot(data=recent_data, x=recent_data.index, y='prices', marker='o', color='orange')
        plt.title('售价随时间变化')
        plt.xlabel('日期')
        plt.ylabel('售价')
        plt.xticks(rotation=45)

        plt.tight_layout()

        # 保存图形为图片
        plt.savefig(f'/home/lighthouse/test_py/Visualization/{file_name}.png')

        # 显示图形
        plt.show()
        return


if __name__ == '__main__':
    runDaemon(api=VisualGraphics())
