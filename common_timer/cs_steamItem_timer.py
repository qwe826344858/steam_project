
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig
from common_tools.mysql import DBHelper

class CS_SteamItem_Timer:
    def test(self):
        commonConfig = CommonConfig()
        mysql_config = commonConfig.getMysqlConfig()

        dbHelper = DBHelper()
        dbHelper.connection()



        print(f"config:{mysql_config}")
        return



if __name__ == '__main__':
    api = CS_SteamItem_Timer()
    api.test()
