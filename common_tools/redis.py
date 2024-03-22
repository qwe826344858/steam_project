import redis

def connect():
    # 创建 Redis 连接
    rds = redis.Redis(host='localhost', port=6379, db=0, password='yourpassword')

    # 检查连接是否成功
    if rds.ping():
        print("Redis 连接成功！")