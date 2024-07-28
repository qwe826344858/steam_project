import grpc
import sys

sys.path.append("/home/lighthouse/test_py")

from pb import hello_pb2_grpc,hello_pb2

req = hello_pb2.req
stub = hello_pb2_grpc.HelloServiceStub


def RunClient():
    with grpc.insecure_channel("localhost:40000") as channel:
        s = stub(channel)
        response = s.sayHello(req(user="i am test"))    # TODO 报错方法未实现
        print(response.response)


if __name__ == '__main__':
    RunClient()
