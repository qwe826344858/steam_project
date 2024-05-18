import json
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig
from common_tools.mysql import DBHelper
from common_tools.loggerHelper import Logger

# 初始化日志
Logger.init()

class CS_SteamItem_Timer:

    database = "Steam_Project"
    table_name = "t_steam_test"

    def test(self):
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

if __name__ == '__main__':
    api = CS_SteamItem_Timer()
    api.testlog()
