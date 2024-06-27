import json
import sys
import datetime
import os
import time

sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig
from common_tools.mysql import DBHelper
from common_tools.loggerHelper import Logger

# 初始化日志
Logger.init()

class CS_SteamItem_Timer:

    database = "Steam_Project"
    table_name = "t_steam_test"
    dbHelper = None

    def test(self):
        table_name = "t_steam_item"
        commonConfig = CommonConfig()
        mysql_config = commonConfig.getMysqlConfig()

        dbHelper = DBHelper(host=mysql_config['host'], username=mysql_config['username'], password=mysql_config['password'], database=self.database,table_name=self.table_name)

        """ 
        # 增
        ext = json.dumps(mysql_config, ensure_ascii=False)
        sql_str_insert = f"INSERT INTO `t_steam_test` (`fuid`,`fext`,`faddtime`) VALUE (12369,'{ext}',1713863931);"
        ret = dbHelper.execute_insert(sql_str_insert)
        if not ret:
            print("CS_SteamItem_Timer 插入数据失败")
            return False
        """


        """
        # 改
        change_uid = 12369
        save_uid = 12311
        sql_str_change = f"UPDATE {self.table_name} SET Fuid = {save_uid} WHERE Fuid = {change_uid}"
        ret = dbHelper.execute_update(sql_str_change)
        if not ret :
            print("CS_SteamItem_Timer 更新数据失败")
            return False
        """


        """
        # 删
        delete_uid = 12311
        sql_str_change = f"DELETE FROM {self.table_name} WHERE Fuid = {delete_uid}"
        ret = dbHelper.execute_delete(sql_str_change)
        if not ret :
            print("CS_SteamItem_Timer 删除数据失败")
            return False
        """

        # 查
        sql_str_select = f"SELECT * FROM {self.table_name} WHERE `Fuid` > 1;"
        ret,data = dbHelper.execute_query(sql_str_select)
        if not ret :
            print("CS_SteamItem_Timer 查询失败")
            return False
        print(f"data:{data}")


        print(f"config:{mysql_config}")
        return True

    def testlog(self):
        Logger.info("只是测试日志哦!")


    def TranFileInfo2DB(self,file_name):
        self.table_name = "t_steam_item"
        strJson = ""
        arr = {}
        # 先读文件
        now = datetime.datetime.now().strftime('%Y%m%d %H:%I:%S')
        Logger.info(f"go open the files! currentTime:{now}")
        # 检查文件是否存在
        if not os.path.exists(file_name):
            Logger(f"文件不存在 file:{file_name}")
            return False

        with open(file_name, "r") as file:
            # 校验文件是否可读
            if not file.readable():
                Logger.info(f"文件不可读,读取失败! file:{file_name}")
                return False

            strJson = file.read()
            if len(strJson) < 1:
                Logger.info(f"空文件! file:{file_name}")
                return True

            arr = json.loads(strJson)

        # 初始化DB
        commonConfig = CommonConfig()
        mysql_config = commonConfig.getMysqlConfig()
        self.dbHelper = DBHelper(host=mysql_config['host'], username=mysql_config['username'], password=mysql_config['password'], database=self.database,table_name=self.table_name)

        Logger.info(f"test run")

        for key,val in arr[0].items():
            key = key.replace("'", "\\'")
            Logger.info(f"key:{key}")
            sql_str_select = f"SELECT * FROM {self.table_name} WHERE `fitem_source_name` = '{key}';"
            ret,data = self.dbHelper.execute_query(sql_str_select)
            if not ret:
                Logger.info(f"CS_SteamItem_Timer 查询失败 sql:{sql_str_select}")
                return False
            Logger.info(f"data:{data}")

            if len(data) == 0:
                addInfo = {
                    'item_source_name':key,
                    'item_cn_name':val.get('item_cn_name',''),
                    'sell_online_count':val.get('sell_online_count',''),
                    'pic_url':val.get('pic_url',''),
                    'show_prices':val.get('show_prices',''),
                    'prices':val.get('prices',''),
                    'currency':val.get('currency',''),
                }
                ret = self.addItemInfo(addInfo)        #插入
                if not ret:
                    continue
            else:
                item_id = self._TranMapBusinessKey(data[0]).get('id')
                Logger.info(f"{item_id}")
                filter = {'id':item_id}
                updateInfo = {
                    'item_cn_name':val.get('item_cn_name',''),
                    'sell_online_count':val.get('sell_online_count',''),
                    'pic_url':val.get('pic_url',''),
                    'show_prices':val.get('show_prices',''),
                    'prices':val.get('prices',''),
                    'currency':val.get('currency',''),
                }
                ret = self.updateItemInfo(filter,updateInfo)     #更新
                if not ret:
                    continue

        return True

    # 记录下当日的商品详情信息
    def everyDayItemInfoWriteDown(self):
        self.table_name = "t_steam_item_single_day_info"
        today = datetime.datetime.now().strftime('%Y%m%d')
        lastID = 0
        while 1:
            ret,dataList = self.getIteamInfoByLastID(lastID,500)
            if not ret:
                Logger.info("everyDayItemInfoWriteDown 查询失败! 结束返回")
                return False

            if len(dataList) == 0:
                break

            lastID = dataList[-1].get('id')
            Logger.info(f"lastID:{lastID}")


            for data in dataList:
                val = data.items()
                addInfo = {
                    'item_id':val.get('id',''),
                    'calc_day':today,
                    'sell_online_count':val.get('sell_online_count',''),
                    'prices':val.get('prices',''),
                    'currency':val.get('currency',''),
                }
                ret = self.addItemInfo(addInfo)
                if not ret:
                    continue

        return True


    def addItemInfo(self,addInfo):
        addInfo['addtime'] = time.time()
        addInfo = self._TranMapTaleKey(addInfo)
        field_str,value_str = self._TranMapKeyAndValues(addInfo)

        sql_str_insert = f"INSERT INTO {self.table_name} ({field_str}) VALUE ({value_str});"
        ret = self.dbHelper.execute_insert(sql_str_insert)
        if not ret:
            Logger.info(f"CS_SteamItem_Timer 插入数据失败 lastSql:{sql_str_insert}")
            return False
        return True

    def updateItemInfo(self,filter,updateInfo):
        filter_str = self._TranMap2Update(self._TranMapTaleKey(filter))
        updateInfo_str = self._TranMap2Update(self._TranMapTaleKey(updateInfo))

        sql_str_change = f"UPDATE {self.table_name} SET {updateInfo_str} WHERE {filter_str} ;"
        ret = self.dbHelper.execute_update(sql_str_change)
        if not ret:
            Logger.info(f"CS_SteamItem_Timer 插入数据失败 lastSql:{sql_str_change}")
            return False
        return True



    def getIteamInfoByLastID(self,lastID,pageSize):
        Logger.info(f"lastID:{lastID}")
        dataList = []
        sql = f"select `fid`,`fsell_online_count`,`fprices`,`fcurrency` from {self.table_name} " \
              f"where fid > {lastID} " \
              f"order by `fid` ASC" \
              f"limit {pageSize}"

        ret,data = self.dbHelper.execute_update(sql)
        if not ret:
            Logger.info(f"getIteamInfoByLastID 查询失败 lastSql:{sql}")
            return False,[]

        for v in data:
            dataList.append(self._TranMapBusinessKey(v))

        return True,dataList


    # 创建sql需要拼接的字段
    def _TranMapKeyAndValues(self,t_dict):
        field_str = "`,`".join(map(str, list(t_dict.keys())))
        field_str = f"`{field_str}`"
        value_str = '","'.join(map(str, list(t_dict.values())))
        value_str = f'"{value_str}"'
        return field_str, value_str

    def _TranMap2Update(self,t_dict):
        str = ""
        for k,v in t_dict.items():
            str += f" `{k}` = '{v}' ,"
        Logger.info(str);
        return str[:len(str)-1]

    # 转义成sql表结构字段
    def _TranMapTaleKey(self,b_dict):
        t_dict = dict(map(lambda k: ('F' + k, b_dict[k]), b_dict))
        return t_dict


    # 转义成业务输出结构字段
    def _TranMapBusinessKey(self,t_dict):
        b_dict = {k[1:]: v for k, v in t_dict.items()}
        return b_dict



if __name__ == '__main__':
    api = CS_SteamItem_Timer()
    #api.testlog()
    fileName = "/home/lighthouse/test_py/cs_project/log.txt"
    api.TranFileInfo2DB(fileName)
