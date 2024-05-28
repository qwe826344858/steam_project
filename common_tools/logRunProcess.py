import threading
import time
import sys
import multiprocessing as mp
sys.path.append("/home/lighthouse/test_py")
from common_tools.redisHelper import get_redis_connection, release_redis_connection, setRedisString, getRedisString, \
    setExpireTime


# 日志守护进程
class logRunProcess:
    # cache_pool = []
    # cache_total_max = 20
    # expire_time = 86400
    # lock = threading.Lock() # 创建锁
    # pathMap = {}

    def __init__(self):
        self.cache_pool = mp.Manager().dict()
        self.cache_total_max = 20
        self.expire_time = 86400
        self.lock = threading.Lock()
        self.pathMap = mp.Manager().dict()

    def addCache(self, context, key ,filePath):
        if len(context) > 65535:
            context = context[0:65534]

        # key不存在时先初始化
        if key not in self.cache_pool:
            self.cache_pool[key] = {}

        self.pathMap[key] = filePath

        self.lock.acquire() # 获取互斥锁
        id = self.idMaker(key)
        if id is not None:
            self.cache_pool[key][id] = context+"\n"
        self.lock.release() # 释放锁
        return

    def idMaker(self, key):
        id = 0
        redis_conn = get_redis_connection()
        ret,value = getRedisString(key)
        if value is None or ret is False:
            value = 0
            setRedisString(key, value, self.expire_time)
        else:
            if id > 9:
                id = 0
            else:
                id = int(chr(int.from_bytes(value,"little"))) + 1           # int.from_bytes 贼恶心,返回的时ascii格式,还要再转义
            setRedisString(key, id, self.expire_time)

        release_redis_connection()  #告警
        print(f"id:{id}")
        return id


    def writeFile(self,path,context):
        print(f"写入文件 path:{path}")
        with open(path, "a") as file:
            file.write(context + "\n")
            file.close()
        return


    def clearCacheByKey(self,key):
        self.lock.acquire() # 获取互斥锁
        self.cache_pool[key] = {}
        self.lock.release()  # 释放锁
        return

    def run(self):
        while 1:
            threads = []
            if not self.cache_pool.items():
                time.sleep(1)
                continue

            for file,logs in self.cache_pool.items():
                context = ""
                if len(logs) < self.cache_total_max:
                    continue

                context = "".join(logs.values())
                thread = threading.Thread(target=self.writeFile, args=(self.pathMap[file], context))
                thread.start()
                threads.append(thread)
                self.clearCacheByKey(file)

            for thread in threads:
                thread.join()

            print(f"休眠1秒 cache_pool:{self.cache_pool}")
            time.sleep(1)


if __name__ == '__main__':
    p = logRunProcess()
    p.run()
