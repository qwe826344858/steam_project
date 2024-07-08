import json
import sys
import datetime
import os
import time
import openpyxl

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
    workbook = None


    def __init__(self):
        # 初始化DB
        commonConfig = CommonConfig()
        mysql_config = commonConfig.getMysqlConfig()
        self.dbHelper = DBHelper(host=mysql_config['host'], username=mysql_config['username'], password=mysql_config['password'], database=self.database,table_name=self.table_name)

    def test(self):
        self.table_name = "t_steam_item"
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

    # 读取文件解析json
    def readJsonFile(self,file_name):
        # 先读文件
        now = datetime.datetime.now().strftime('%Y%m%d %H:%I:%S')
        Logger.info(f"go open the files! currentTime:{now}")
        # 检查文件是否存在
        if not os.path.exists(file_name):
            Logger(f"文件不存在 file:{file_name}")
            return False,None

        with open(file_name, "r") as file:
            # 校验文件是否可读
            if not file.readable():
                Logger.info(f"文件不可读,读取失败! file:{file_name}")
                return False,None

            strJson = file.read()
            if len(strJson) < 1:
                Logger.info(f"空文件! file:{file_name}")
                return False,None

            arr = json.loads(strJson)

        return True,arr


    # 将文件中的信息转换后写入DB
    def TranFileInfo2DB(self):
        file_name = "/home/lighthouse/test_py/cs_project/log.txt"
        self.table_name = "t_steam_item"
        ret,arr = self.readJsonFile(file_name)
        if not ret or arr is None:
            return False

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
                ret = self.addInfo(addInfo)        #插入
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
                ret = self.updateInfo(filter,updateInfo)     #更新
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
                Logger.info("getIteamInfoByLastID 查询失败! 结束返回")
                return False

            if len(dataList) == 0:
                break

            lastID = dataList[-1].get('id')
            Logger.info(f"lastID:{lastID}")


            # 查询商品记录
            for item_info in dataList:
                val = item_info
                itemId = val.get("id",'')

                # 如果自增的唯一主键都取不出来值,是否是数据转义时生产的脏记录
                # if itemId == '':
                #     Logger.info(f"商品id为空! 跳过 name:{val.get('item_cn_name','')}")
                #     continue

                # 这里需要先查询今日是否有过添加记录,有则更新，没有则新增
                item_filter = {
                    "item_id":itemId,
                    "calc_day":today,
                }
                ret,today_record = self.getSingleInfo(item_filter)
                if not ret:
                    Logger.info(f"getSingleInfo 查询失败! filter:{item_filter}")
                    return False

                addInfo = {
                    'item_id': itemId,
                    'calc_day': today,
                    'sell_online_count': val.get('sell_online_count', ''),
                    'prices': val.get('prices', ''),
                    'currency': val.get('currency', ''),
                }
                if today_record == []:
                    ret = self.addInfo(addInfo)
                    if not ret:
                        continue
                else:
                    item_day_id = today_record.get("id",'')
                    day_filter = {'id':item_day_id}

                    del addInfo['item_id']
                    del addInfo['calc_day']
                    ret = self.updateInfo(day_filter,addInfo)
                    if not ret:
                        continue

        return True


    # 将文件中的信息转换后写入excel
    def TranItemInfo2Excel(self):
        today = datetime.datetime.now().strftime('%Y%m%d')
        self.table_name = "t_steam_item_single_day_info"

        lastID = 0
        while 1:
            ret,dataList = self.getIteamInfoByLastID(lastID,500)
            if not ret:
                Logger.info("getIteamInfoByLastID 查询失败! 结束返回")
                return False

            if len(dataList) == 0:
                break

            for id in self.array_column(dataList,'id'):
                filter = {}
                filter['item_id'] = id
                ret,everyDayDataList = self.getInfo(filter=filter,page=1,pageSize=5000)
                if not ret:
                    Logger.info("getInfo 查询失败! 结束返回")
                    return False

                Logger.info(f"everyDayDataList:{everyDayDataList}")
                val = everyDayDataList
                self._TransAnalyzeExcelFile(val,id,today)

            lastID = dataList[-1].get('id')
            Logger.info(f"lastID:{lastID}")

        return True




# 下面是非入口方法
    # ----------------------------------------------------------------------------------------

    # 只找单条记录了 (common)
    def getSingleInfo(self,filter,order = "fid ASC"):
        ret,dataList = self.getInfo(filter=filter,page=1,pageSize=1,order=order)
        if not ret:
            return False,[]

        if dataList == []:
            return True,dataList

        return ret,dataList[0]

    # 找出所有的记录 (common)
    def getInfo(self,filter,page = 1,pageSize = 50,order = "fid ASC"):
        dataList = []
        filter_str = self._TranMap2Filter(filter)
        sql = f"SELECT * FROM {self.table_name} WHERE {filter_str} ORDER BY {order} LIMIT {(page-1)*pageSize},{pageSize};"
        ret, data = self.dbHelper.execute_query(sql)
        if not ret:
            Logger.info(f"查询失败 table:{self.table_name} sql:{sql}")
            return False,[]

        if len(data) == 0:
            return True,[]

        for v in data:
            dataList.append(self._TranMapBusinessKey(v))

        return True,dataList


    # 添加记录 (common)
    def addInfo(self,addInfo):
        addInfo['addtime'] = time.time()
        addInfo = self._TranMapTaleKey(addInfo)
        field_str,value_str = self._TranMapKeyAndValues(addInfo)

        sql_str_insert = f"INSERT INTO {self.table_name} ({field_str}) VALUE ({value_str});"
        ret = self.dbHelper.execute_insert(sql_str_insert)
        if not ret:
            Logger.info(f"CS_SteamItem_Timer 插入数据失败 lastSql:{sql_str_insert}")
            return False
        return True

    # 更新记录 (common)
    def updateInfo(self,filter,updateInfo):
        filter_str = self._TranMap2Update(self._TranMapTaleKey(filter))
        updateInfo_str = self._TranMap2Update(self._TranMapTaleKey(updateInfo))

        sql_str_change = f"UPDATE {self.table_name} SET {updateInfo_str} WHERE {filter_str} ;"
        ret = self.dbHelper.execute_update(sql_str_change)
        if not ret:
            Logger.info(f"CS_SteamItem_Timer 插入数据失败 lastSql:{sql_str_change}")
            return False

        Logger.info(f"更新记录成功! filter:{filter} updateInfo:{updateInfo}")
        return True



    def getIteamInfoByLastID(self,lastID,pageSize):
        Logger.info(f"lastID:{lastID}")
        dataList = []
        sql = f"select `fid`,`fsell_online_count`,`fprices`,`fcurrency` from `t_steam_item`" \
              f"where fid > {lastID} " \
              f"order by `fid` ASC " \
              f"limit {pageSize};"

        ret,data = self.dbHelper.execute_query(sql)
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
        return str[:len(str)-1]

    # 查询时where的条件拼接
    def _TranMap2Filter(self, t_dict):
        str = ""
        for k, v in t_dict.items():
            if isinstance(v,list):
                extStr = "', '".join([format(single) for single in v])
                str += f" `f{k}` IN ('{extStr}') AND"
            else:
                str += f" `f{k}` = '{v}' AND"
        return str[:len(str) - 3]

    # 转义成sql表结构字段
    def _TranMapTaleKey(self,b_dict):
        t_dict = dict(map(lambda k: ('F' + k, b_dict[k]), b_dict))
        return t_dict


    # 转义成业务输出结构字段
    def _TranMapBusinessKey(self,t_dict):
        b_dict = {k[1:]: v for k, v in t_dict.items()}
        return b_dict


    def _TransAnalyzeExcelFile(self,arr,item_id,day):
        # 创建一个新的Excel工作簿
        self.workbook = openpyxl.Workbook()

        # 获取活动的工作表
        sheet = self.workbook.active
        index = 1

        # 写入数据到单元格
        sheet[f"A{index}"] ="日期"
        sheet[f"B{index}"] ="商品价格"
        sheet[f"C{index}"] ="在售的数量"


        for val in arr:
            index += 1
            Logger.info(f"val:{val}")
            sheet[f"A{index}"] = val.get("calc_day")
            sheet[f"B{index}"] = val.get("prices","0")
            sheet[f"C{index}"] = val.get("sell_online_count","0")

        # 保存Excel文件
        self.workbook.save(fr"/home/lighthouse/test_py/ExcelFile/output_{item_id}.xlsx")


    def array_column(self,arr, col):
        retList = []
        for item in arr:
            retList.append(item.get(col))
        return retList


if __name__ == '__main__':
    # 通过命令行输入方法名进行调用
    method_name  = sys.argv[1]     # 获取命令中第一个额外参数
    api = CS_SteamItem_Timer()

    # 获取方法对象
    method = getattr(api, method_name, None)

    # 检查方法是否存在
    if method is None or not callable(method):
        print(f"方法 '{method_name}' 不存在或不可调用")
        sys.exit(1)

    # 调用方法
    method()
