
# 在所有通过proto生成的文件中 hello_pb2_grpc.py 需要加上其系统引用路径
import sys
sys.path.append("/home/lighthouse/test_py")

# 或者在对应包的目录下新增__init__.py文件,这样就不需要声明引用路径了

# 一定要确保所有服务端和客户端的proto文件要一致
否则会出现跨语言之间服务调不通的情况