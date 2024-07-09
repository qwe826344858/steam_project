import datetime
import inspect
import os
import multiprocessing as mp
import sys
import time

sys.path.append("/home/lighthouse/test_py")
from common_tools.redisHelper import get_redis_connection, release_redis_connection, getRedisString, setRedisString,delRedisString
from common_tools.commonConfig import CommonConfig

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

        logger = Logger()
        logger.run(log_message=log_message)
        # asyncio.run(self.process_info(log_message))


    def run(self,log_message):
        p = mp.Process(target=self.addInfo(log_message=log_message))
        p.start()
        p.join()


    def addInfo(self, log_message):
        self.cache_pool.append(log_message)
        if len(self.cache_pool) > self.cache_pool_max_log:
            self.updateLog2file()
            self.cache_pool.clear()

        return

    def updateLog2file(self):
        dirPath = f"{Logger.log_config['save_path']}/{Logger.log_day}"
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)

        # 检查文件是否存在
        if not os.path.exists(self.save_path):
            # 创建文件
            open(self.save_path, "a").close()

        self.writeFile()
        return


    def writeFile(self):
        if self.log_config['distributed']:
            self.writeFileByDistributed()
        else:
            self.writeFileBySingleService()
        return


    def writeFileByDistributed(self):
        redis_conn = get_redis_connection()
        start_time = time.time()
        retry_count = 0
        logMessage = "\n".join(self.cache_pool)
        delRDSState = False
        while 1:

            if time.time() - start_time > 60:
                print(f"time out!  give up this log:{logMessage}")
                break

            ret,str = getRedisString(self.basename)    # TODO
            if not ret:
                print(f"call redis is failed! key:{self.basename}")
                break

            if str != "":
                time.sleep(1)  # 1s后再试
                continue
            else:
                setRedisString(self.basename,"1",60)
                delRDSState = True


            try:
                with open(self.save_path, "a") as file:
                    file.write(logMessage)
                    if delRDSState:
                        delRedisString(self.basename)
                    break
            except IOError as e:
                print(f"writeFileByDistributed retry_count:{retry_count} err:{e}")
                retry_count += 1


            time.sleep(1)       # 1s后再试

        release_redis_connection(redis_conn)

    def writeFileBySingleService(self):
        retry_count = 0
        logMessage = "\n".join(self.cache_pool)
        while 1:
            try:
                with open(self.save_path, "a") as file:
                    file.write(logMessage)
                    break
            except IOError as e:
                print(f"writeFileBySingleService retry_count:{retry_count} err:{e}")
                if retry_count >= self.log_config["retry_max"]:
                    break
                retry_count += 1
                time.sleep(1)   # 1s后再试

    def __del__(self):
        if len(self.cache_pool) != 0:
            self.updateLog2file()
            self.cache_pool.clear()
