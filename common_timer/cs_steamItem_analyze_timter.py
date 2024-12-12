import sys
import datetime
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

from common_tools.envPythonConfig import getEnvConfig

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
        commonConfig = getEnvConfig()
        mysql_config = commonConfig.get("mysql_conf")
        self.dbHelper = DBHelper(host=mysql_config['host'], username=mysql_config['username'], password=mysql_config['password'], database=self.database,table_name=self.table_name)


    def runAnalyze(self):
        if len(sys.argv) > 2:
            fileName = fr'/home/lighthouse/test_py/ExcelFile/output_{int(sys.argv[2])}.xlsx'
            ret = self.runAnalyzeItemInfo(fileName)
            if not ret:
                print("读取文件启动预测失败!")
                return False
        else:
            print(f"type:{sys.argv[2]}")
        return

    # 分析文件
    def runAnalyzeItemInfo(self,fileName):
        # 读取数据
        today = datetime.datetime.now().strftime('%Y%m%d')
        next_day = datetime.datetime.now() + datetime.timedelta(days=1)
        tomorrow = next_day.strftime('%Y%m%d')
        data = pd.read_excel(fileName)

        # 商品价格预测
        # 数据预处理
        data["日期"] = pd.to_datetime(data["日期"], format="%Y%m%d")
        data["日期_num"] = (data["日期"] - data["日期"].min()).dt.days  # 将日期转换为数值型

        # 划分训练集和测试集
        X_train, X_test, y_train_price, y_test_price, y_train_quantity, y_test_quantity = train_test_split(
            data[["日期_num"]], data["商品价格"], data["在售的数量"], test_size=0.2, random_state=42)

        # 价格预测模型
        price_model = LinearRegression()
        price_model.fit(X_train, y_train_price)
        price_pred = price_model.predict(X_test)
        price_mse = mean_squared_error(y_test_price, price_pred)
        price_r2 = r2_score(y_test_price, price_pred)
        print(f"Price Prediction: MSE = {price_mse:.2f}, R-squared = {price_r2:.2f}")

        # 在售数量预测模型
        quantity_model = LinearRegression()
        quantity_model.fit(X_train, y_train_quantity)
        quantity_pred = quantity_model.predict(X_test)
        quantity_mse = mean_squared_error(y_test_quantity, quantity_pred)
        quantity_r2 = r2_score(y_test_quantity, quantity_pred)
        print(f"Quantity Prediction: MSE = {quantity_mse:.2f}, R-squared = {quantity_r2:.2f}")

        # 预测未来数据
        future_date = pd.to_datetime(f"{tomorrow}", format="%Y%m%d")
        future_date_num = (future_date - data["日期"].min()).days
        future_price = price_model.predict([[future_date_num]])
        future_quantity = quantity_model.predict([[future_date_num]])

        print(f"预测商品价格: {future_price[0]}")
        print(f"预测在售数量: {future_quantity[0]}")

        return True

if __name__ == '__main__':
    # 通过命令行输入方法名进行调用
    method_name = sys.argv[1]     # 获取命令中第一个额外参数
    api = CS_SteamItem_Analyze_Timer()

    # 获取方法对象
    method = getattr(api, method_name, None)

    # 检查方法是否存在
    if method is None or not callable(method):
        print(f"方法 '{method_name}' 不存在或不可调用")
        sys.exit(1)

    # 调用方法
    method()
