import redis

# 创建 Redis 连接池
pool = redis.ConnectionPool(host='localhost', port=6379, db=0)

# 获取 Redis 连接
def get_redis_connection():
    return redis.Redis(connection_pool=pool)

# 释放 Redis 连接
def release_redis_connection(connection):
    connection.close()


if __name__ == '__main__':
    # 使用连接池进行 Redis 操作
    redis_conn = get_redis_connection()
    redis_conn.set('key', 'value')
    print(redis_conn.get('key'))
    release_redis_connection(redis_conn)