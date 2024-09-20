import time

from common_tools.loggerHelper import Logger
from common_dao import CommonDao

Logger.init()
class ItemDao(CommonDao):
    database = "Steam_Project"
    table_name = "t_steam_item"

    TABLE_ITEM = "t_steam_item"
    TABLE_ITEM_SINGLE_DAY = "t_steam_item_single_day_info"

    def SetTable(self,table):
        self.table_name = table

    def SetDataBase(self,database):
        self.database = database

    # 分批获取数据
    def getIteamInfoByLastID(self, lastID, pageSize, field="*"):
        Logger.info(f"lastID:{lastID}")
        dataList = []
        sql = f"select * from {self.table_name}" \
              f"where fid > {lastID} " \
              f"order by `fid` ASC " \
              f"limit {pageSize};"

        ret, data = self.dbHelper.execute_query(sql)
        if not ret:
            Logger.info(f"getIteamInfoByLastID 查询失败 lastSql:{sql}")
            return False, []

        for v in data:
            dataList.append(self._TranMapBusinessKey(v))

        return True, dataList

    # 只找单条记录了 (common)
    def getSingleInfo(self, filter, order="fid ASC"):
        ret, dataList = self.getInfo(filter=filter, page=1, pageSize=1, order=order)
        if not ret:
            return False, []

        if dataList == []:
            return True, dataList

        return ret, dataList[0]

    # 找出所有的记录 (common)
    def getInfo(self, filter, page=1, pageSize=50, order="fid ASC"):
        dataList = []
        filter_str = self._TranMap2Filter(filter)
        sql = f"SELECT * FROM {self.table_name} WHERE {filter_str} ORDER BY {order} LIMIT {(page - 1) * pageSize},{pageSize};"
        ret, data = self.dbHelper.execute_query(sql)
        if not ret:
            Logger.info(f"查询失败 table:{self.table_name} sql:{sql}")
            return False, []

        if len(data) == 0:
            return True, []

        for v in data:
            dataList.append(self._TranMapBusinessKey(v))

        return True, dataList

    # 添加记录 (common)
    def addInfo(self, addInfo):
        addInfo['addtime'] = time.time()
        addInfo = self._TranMapTaleKey(addInfo)
        field_str, value_str = self._TranMapKeyAndValues(addInfo)

        sql_str_insert = f"INSERT INTO {self.table_name} ({field_str}) VALUE ({value_str});"
        ret = self.dbHelper.execute_insert(sql_str_insert)
        if not ret:
            Logger.info(f"CS_SteamItem_Timer 插入数据失败 lastSql:{sql_str_insert}")
            return False
        return True

    # 更新记录 (common)
    def updateInfo(self, filter, updateInfo):
        filter_str = self._TranMap2Update(self._TranMapTaleKey(filter))
        updateInfo_str = self._TranMap2Update(self._TranMapTaleKey(updateInfo))

        sql_str_change = f"UPDATE {self.table_name} SET {updateInfo_str} WHERE {filter_str} ;"
        ret = self.dbHelper.execute_update(sql_str_change)
        if not ret:
            Logger.info(f"CS_SteamItem_Timer 插入数据失败 lastSql:{sql_str_change}")
            return False

        Logger.info(f"更新记录成功! filter:{filter} updateInfo:{updateInfo}")
        return True
