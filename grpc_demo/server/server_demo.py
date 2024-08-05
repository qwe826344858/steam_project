from concurrent import futures
import grpc
import sys

sys.path.append("/home/lighthouse/test_py")

from grpc_demo.pb import hello_pb2_grpc,hello_pb2

req = hello_pb2.req
resp = hello_pb2.resp
server = hello_pb2_grpc.HelloServiceServicer
_rpc = hello_pb2_grpc

class DemonServer(server):
    def SayHello(self, request, context):
        user = request.user
        print(f"user:{user} has call this")
        return resp(msg=f"hello {user}")



def StartService():
    port = "40000"
    gs = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    hello_pb2_grpc.add_HelloServiceServicer_to_server(DemonServer(), gs)
    gs.add_insecure_port('[::]:' + port)
    gs.start()
    print("Server started, listening on " + port)
    gs.wait_for_termination()

if __name__ == '__main__':
    StartService()