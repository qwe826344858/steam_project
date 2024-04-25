import datetime
import inspect
import os
import asyncio
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig

# TODO 待验证
class Logger:
    log = None
    log_file_path = ''
    log_file_name = ''
    log_config = {}
    save_path = ''

    # 日志的缓存池 减少文件操作 当日志数量达到阈值时会异步写入到文件中
    cache_pool = []

    @staticmethod
    def init():
        if Logger.log is not None:
            return

        caller_frame = inspect.currentframe().f_back
        file_info = inspect.getframeinfo(caller_frame)
        log_file_name = file_info.filename

        Logger.log_file_path = os.path.abspath(log_file_name)
        Logger.log_config = CommonConfig.getLogConfig()
        Logger.save_path = f"{Logger.log_config['save_path']}/{datetime.datetime.now().date()}/"


    # 日志调用入口
    def info(self, message):
        current_time = datetime.datetime.now()
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)
        self.save_path += f"{caller_info.filename}"

        log_message = f"[{current_time}] {message}"
        log_message += f" | path:{self.log_file_path} Called from {caller_info.filename}, {caller_info.function}(), Line {caller_info.lineno}"

        asyncio.run(self.process_info(log_message))


    # 异步写入文件
    async def write_to_file(self, message):
        # 异步写入文件的逻辑
        await asyncio.sleep(1)  # 模拟异步写入操作
        print(f"Message '{message}' written to file")
        async with open(self.log_file, "a") as file:
            await file.write(message + "\n")

    async def process_info(self, message):
        if len(self.cache_pool) >= 20:  # 当日志数量达到阈值时
            await self.flush_log_cache()  # 异步写入缓存池中的日志

        self.cache_pool.append(message)

    async def flush_log_cache(self):
        tasks = []
        for message in self.cache_pool:
            task = asyncio.ensure_future(self.write_to_file(message))
            tasks.append(task)

        await asyncio.gather(*tasks)  # 并行执行所有异步写入任务
        self.cache_pool.clear()  # 清空缓存池
