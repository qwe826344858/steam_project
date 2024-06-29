import datetime
import inspect
import os
import multiprocessing as mp
import sys

sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig
from common_tools.logRunProcess import logRunProcess

# 搞定力
class Logger:
    log = None
    log_file_path = ''
    log_file_name = ''
    log_config = {}
    save_path = ''
    log_day = ''
    current_file_name = ''
    current_file_path = ''
    basename = ''

    # 日志的缓存池 减少文件操作 当日志数量达到阈值时会异步写入到文件中
    cache_pool = []
    cache_pool_max_log = 20

    @staticmethod
    def init():
        if Logger.log is not None:
            return

        caller_frame = inspect.currentframe().f_back
        file_info = inspect.getframeinfo(caller_frame)
        log_file_name = file_info.filename
        Logger.log_day = datetime.datetime.now().strftime('%Y%m%d')

        Logger.log_file_path = os.path.abspath(log_file_name)
        Logger.log_config = CommonConfig.getLogConfig()
        Logger.current_file_name = os.path.basename(log_file_name)
        Logger.save_path = f"{Logger.log_config['save_path']}/{Logger.log_day}/{Logger.current_file_name}.log"

    def resetSavePath(self):
        Logger.log_day = datetime.datetime.now().strftime('%Y%m%d')
        Logger.save_path = f"{Logger.log_config['save_path']}/{Logger.log_day}/{Logger.current_file_name}.log"

    # 日志调用入口
    @staticmethod
    def info(message):
        if Logger.log_day != datetime.datetime.now().strftime('%Y%m%d'):
            Logger.resetSavePath(Logger)

        current_time = datetime.datetime.now()
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)
        Logger.basename = os.path.basename(caller_info.filename) #文件名称（不带路径）
        Logger.current_file_path = os.path.dirname(os.path.abspath(__file__))

        log_message = f"[{current_time}] "
        log_message += f"path:{Logger.log_file_path} Called from {caller_info.filename}, {caller_info.function}(), Line {caller_info.lineno}"
        log_message += f" output ==> {message}"

        print(f"写日志 message:{message}")
        logger = Logger()
        logger.run(log_message=log_message)
        # asyncio.run(self.process_info(log_message))


    def run(self,log_message):
        p = mp.Process(target=self.addInfo(log_message=log_message))
        p.start()
        p.join()


    def addInfo(self, log_message):
        self.cache_pool.append(log_message)
        print("addInfo")
        if len(self.cache_pool) > self.cache_pool_max_log:
            print("输出日志到文件中")
            self.updateLog2file()
            self.cache_pool.clear()

        return

    def updateLog2file(self):
        dirPath = f"{Logger.log_config['save_path']}/{Logger.log_day}"
        if not os.path.exists(dirPath):
            print(f"目录不存在 path:{dirPath}")
            os.makedirs(dirPath)

        # 检查文件是否存在
        if not os.path.exists(self.save_path):
            print(f"文件不存在 file:{self.save_path}")
            # 创建文件
            open(self.save_path, "a").close()

        with open(self.save_path, "a") as file:
            for log in self.cache_pool:
                file.write(log + "\n")
        return

    def __del__(self):
        if len(self.cache_pool) != 0:
            print("__del__ 输出日志到文件中")
            self.updateLog2file()
            self.cache_pool.clear()
