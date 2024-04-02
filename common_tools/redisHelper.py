import redis
from tools import getCurrentFileInfo, getCurrentMethodName, setReturn, initSet

errCode = 0
errMsg = "success"
pool = None
redis_connect = None
current_file_name = ""
current_file_path = ""
current_file_method = ""

# redis 链接配置
redis_host = 'localhost'
redis_port = 6379
redis_db = 0
expire_time = 2592000  # redis 默认过期时间


# 构造函数
def __init__(pool_connect=None):
    global current_file_name, current_file_path
    current_file_name, current_file_path = getCurrentFileInfo()


# 创建redis的链接实例
def initConnect(pool_connect):
    global pool  # 声明全局变量
    try:
        # 是否已创建连接实例了？
        if not pool_connect:
            # Redis 连接池申请连接
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, db=redis_db)
        else:
            pool = pool_connect
    except Exception as e:
        print(f"redis创建连接! pool_connect:{pool_connect} errMsg:{e}")
        return False,None

    return True,pool


# 获取 Redis 连接
def get_redis_connection():
    global redis_connect
    try:
        redis_connect = redis.Redis(connection_pool=pool)
    except Exception as e:
        print(f"获取redis对象失败!errMsg:{e}")
        return False, None

    return True, redis_connect


# 释放 Redis 连接
def release_redis_connection(redis_connect):
    try:
        redis_connect.close()
    except Exception as e:
        print(f"关闭redis连接失败!errMsg:{e}")
        return False

    return True


# 设置字符串
def setRedisString(name,value, expire=expire_time):
    redis_connect.set(name=name, value=value,expire=expire)
    return True


# 获取字符串
def getRedisString(name):
    str = redis_connect.get(name)
    return True, str


# 删除字符串
def delRedisString(name):
    ret = redis_connect.delete(name)
    print(f"{getCurrentMethodName()} ret:{ret}")
    if ret == 1:
        print(f"删除string name 成功! name:{name}")
        return True
    else:
        print(f"删除string name 失败! name:{name}")
        return False


# 设置Hash key和value
def setRedisHash(name, key, value, expire=expire_time):
    ret = redis_connect.hset(name=name,key=key, value=value, expire=expire)
    print(f"{getCurrentMethodName()} ret:{ret}")
    return True


# 获取Hash value
def getRedisHash(name, key):
    try:
        obj = redis_connect.hget(name,key)
        return True, obj
    except Exception as e:
        print(f"{getCurrentMethodName()} 获取Hash value失败! name:{name} key:{key} errMsg:{e}")
        return False,{}


# 获取Hash 所有的key和value
def getRedisAllHash(name):
    try:
        arr = redis_connect.hgetall(name)
        return True, arr
    except Exception as e:
        print(f"{getCurrentMethodName()} 获取所有Hash value失败! name:{name} errMsg:{e}")
        return False,[]


# 删除 Hash对应的key
def delRedisHash(name, key):
    try:
        ret = redis_connect.hdel(name,key)
    except Exception as e:
        print(f"{getCurrentMethodName()} 删除Hash value失败! name:{name} key:{key} errMsg:{e}")
        return False

    return True

# 设置过期时间
def setExpireTime(name,expire_time):
    if expire_time == 0:
        ret = redis_connect.persist(name)
    else:
        ret = redis_connect.expire(name,expire_time)


    print(f"{getCurrentMethodName()} name:{name} expire_time:{expire_time} ret:{ret}")
    return True

# if __name__ == '__main__':
#     # 使用连接池进行 Redis 操作
#     redis_conn = get_redis_connection()
#     redis_conn.set('key', 'value')
#     print(redis_conn.get('key'))
#     release_redis_connection(redis_conn)
