import sys
import pandas as pd
from sklearn.linear_model import LinearRegression

sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig
from common_tools.mysql import DBHelper
from common_tools.loggerHelper import Logger

# 初始化日志
Logger.init()

class CS_SteamItem_Analyze_Timer:

    database = "Steam_Project"
    table_name = ""
    dbHelper = None

    def __init__(self):
        # 初始化DB
        commonConfig = CommonConfig()
        mysql_config = commonConfig.getMysqlConfig()
        self.dbHelper = DBHelper(host=mysql_config['host'], username=mysql_config['username'], password=mysql_config['password'], database=self.database,table_name=self.table_name)


    def runAnalyzeItemInfo(self):
        # 读取数据
        data = pd.read_excel('/home/lighthouse/test_py/cs_project/商品统计数据.xlsx')

        # 数据预处理
        X = data[['日期', '在售的数量']]  # 特征
        y = data['商品价格']  # 标签

        # 创建线性回归模型
        model = LinearRegression()
        model.fit(X, y)

        # 预测新数据
        new_data = pd.DataFrame({'日期': ['2023-06-01'], '在售的数量': [100]})
        predicted_price = model.predict(new_data)
        print(f"预测价格: {predicted_price[0]}")



if __name__ == '__main__':
    # 通过命令行输入方法名进行调用
    method_name  = sys.argv[1]     # 获取命令中第一个额外参数
    api = CS_SteamItem_Analyze_Timer()

    # 获取方法对象
    method = getattr(api, method_name, None)

    # 检查方法是否存在
    if method is None or not callable(method):
        print(f"方法 '{method_name}' 不存在或不可调用")
        sys.exit(1)

    # 调用方法
    method()
