import threading
import time
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.redisHelper import get_redis_connection, release_redis_connection, setRedisString, getRedisString, \
    setExpireTime


# 日志守护进程
class logRunProcess:
    cache_pool = []
    cache_total_max = 20
    expire_time = 86400
    lock = threading.Lock() # 创建锁


    def addCache(self, context, key):
        if len(context) > 65535:
            context = context[0:65534]

        self.lock.acquire() # 获取互斥锁
        self.cache_pool[key][self.idMaker(key)] = context+"\n"
        self.lock.release() # 释放锁
        return

    def idMaker(self, key):
        ret = 0
        redis_conn = get_redis_connection()
        value = getRedisString(key)
        if value is None or value == "":
            value = 0
            setRedisString(key, value, self.expire_time)
        else:
            value += 1
            setRedisString(key, value, self.expire_time)
            ret = getRedisString(key)
            if ret is None or ret is False:
                ret = 0

        release_redis_connection()
        return ret


    def writeFile(self,path,context):
        with open(path, "a") as file:
            file.write(context + "\n")
            file.close()
        return


    def clearCacheByKey(self,key):
        self.lock.acquire() # 获取互斥锁
        self.cache_pool[key] = []
        self.lock.release()  # 释放锁
        return

    def run(self):
        while 1:
            threads = []
            for file,logs in self.cache_pool.items():
                context = ""
                if len(logs) < self.cache_total_max:
                    continue

                context = "".join(logs.values())
                thread = threading.Thread(target=self.writeFile, args=(file, context))
                thread.start()
                threads.append(thread)
                self.clearCacheByKey(file)

            for thread in threads:
                thread.join()

        time.sleep(1)


if __name__ == '__main__':
    p = logRunProcess()
    p.run()
