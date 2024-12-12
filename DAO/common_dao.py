from common_tools.envPythonConfig import getEnvConfig
from common_tools.loggerHelper import Logger
from common_tools.commonConfig import CommonConfig
from common_tools.mysql import DBHelper

Logger.init()
class CommonDao:
    database = "Steam_Project"
    table_name = "t_steam_test"
    dbHelper = None
    mysql_config = {}


    def __init__(self):
        # 初始化DB
        commonConfig = getEnvConfig()
        self.mysql_config = commonConfig.get("mysql_conf")
        self.dbHelper = DBHelper(
            host=self.mysql_config['host'],
            username=self.mysql_config['username'],
            password=self.mysql_config['password'],
            database=self.database,
            table_name=self.table_name)



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



    def array_column(self,arr, col):
        retList = []
        for item in arr:
            retList.append(item.get(col))
        return retList