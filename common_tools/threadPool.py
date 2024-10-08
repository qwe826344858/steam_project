import threading
import queue

from common_tools.loggerHelper import Logger
from common_tools.tools import GetThreadCountByCore

Logger.init()


class ThreadPool:
    def __init__(self, max_workers):
        self.tasks = queue.Queue()
        self.threads = []
        self.shutdown_flag = threading.Event()

        if not max_workers:
            max_workers = GetThreadCountByCore
            Logger.info(f"无指定线程池大小,默认按系统分配 max_workers:{max_workers}")

        for _ in range(max_workers):
            thread = threading.Thread(target=self.run)
            thread.start()
            self.threads.append(thread)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.wait()

    # 执行
    def run(self):
        while not self.shutdown_flag.is_set():
            try:
                task, args, kwargs = self.tasks.get(timeout=1)
                task(*args, **kwargs)
            except queue.Empty:
                continue

    # 注册一个线程
    # *args: 这是一个可变参数，允许你传递任意数量的位置参数
    # **kwargs: 这是一个可变关键字参数，允许你传递任意数量的关键字参数
    def submit(self, task, *args, **kwargs):
        Logger.info(f"debug task:{task}")
        self.tasks.put((task, args, kwargs))

    # 等待线程结束
    def wait(self):
        self.shutdown_flag.set()
        for thread in self.threads:
            thread.join()

    ## 使用方式
    # with ThreadPool(max_workers = 5) as tp:
    #   tp.submit(func(),param)
