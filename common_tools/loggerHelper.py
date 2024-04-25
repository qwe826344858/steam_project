import datetime
import inspect
import os
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig


class Logger:
    log = None
    log_file_path = ''
    log_file_name = ''

    @staticmethod
    def init():
        if Logger.log is not None:
            return

        caller_frame = inspect.currentframe().f_back
        file_info = inspect.getframeinfo(caller_frame)
        log_file_name = file_info.filename
        Logger.log_file_path = os.path.abspath(log_file_name)
        Logger.log_file = f"{CommonConfig.getLogConfig()}"



    def info(self, message):
        current_time = datetime.datetime.now()
        caller_frame = inspect.currentframe().f_back
        caller_info = inspect.getframeinfo(caller_frame)

        log_message = f"[{current_time}] {message}"
        log_message += f" | path:{self.log_file_path} Called from {caller_info.filename}, {caller_info.function}(), Line {caller_info.lineno}"

        with open(self.log_file, "a") as file:
            file.write(log_message + "\n")