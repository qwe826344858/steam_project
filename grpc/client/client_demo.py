import grpc
import sys

sys.path.append("/home/lighthouse/test_py")

from pb import hello_pb2_grpc,hello_pb2

req = hello_pb2.req
stub = hello_pb2_grpc.HelloServiceStub


def RunClient():
    try:
        with grpc.insecure_channel("localhost:40000") as channel:
            s = hello_pb2_grpc.HelloServiceStub(channel)
            param = hello_pb2.req(user="zoneslee")
            try:
                resp = s.sayHello(param)
                print(resp.msg)    # 内容与proto中定义 resp 一致
            except grpc.RpcError as e:
                print(f"gRPC call failed with error: {e.code()}: {e.details()}")
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    print("Server unavailable. Please check if the server is running and reachable.")
                raise e
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == '__main__':
    RunClient()
