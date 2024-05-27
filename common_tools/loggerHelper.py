import datetime
import inspect
import os
import asyncio
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig
from common_tools.logRunProcess import logRunProcess

# TODO 待验证
class Logger:
    log = None
    log_file_path = ''
    log_file_name = ''
    log_config = {}
    save_path = ''
    log_day = ''
    current_file_name = ''

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
    def info(self, message):
        if self.log_day != datetime.datetime.now().strftime('%Y%m%d'):
            self.resetSavePath(self)

        current_time = datetime.datetime.now()
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        log_message = f"[{current_time}] {message}"
        log_message += f" | path:{self.log_file_path} Called from {caller_info.filename}, {caller_info.function}(), Line {caller_info.lineno}"

        print(f"写日志 message:{message}")
        log = logRunProcess()
        log.addCache(context=log_message,key=Logger.save_path)
        #asyncio.run(self.process_info(log_message))


    # # 异步写入文件
    # @classmethod
    # async def write_to_file(cls, message):
    #     # 异步写入文件的逻辑
    #     await asyncio.sleep(0)  # 模拟异步写入操作
    #     print(f"Message '{message}' written to file")
    #     async with open(cls.save_path, "a") as file:
    #         await file.write(message + "\n")
    #
    # @classmethod
    # async def process_info(cls, message):
    #     if len(cls.cache_pool) >= cls.cache_pool_max_log:  # 当日志数量达到阈值时
    #         await cls.flush_log_cache()  # 异步写入缓存池中的日志
    #
    #     cls.cache_pool.append(message)
    #
    # @classmethod
    # async def flush_log_cache(cls):
    #     tasks = []
    #     for message in cls.cache_pool:
    #         task = asyncio.ensure_future(cls.write_to_file(message))
    #         tasks.append(task)
    #
    #     await asyncio.gather(*tasks)  # 并行执行所有异步写入任务
    #     cls.cache_pool.clear()  # 清空缓存池
