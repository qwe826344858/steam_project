import os
import time

import grpc
from grpc_demo.pb import hello_pb2_grpc,hello_pb2

class GrpcSavingDaemon():
    daemon_log_txt = "python_grpc_daemon_stdout.log"

    def run(self):
        while True:
            self.CheckService()
            time.sleep(1800)
        return

    def CheckService(self):
        # 给grpc服务发送请求
        ret = self.RunHelloClient()
        if ret is False:
            self.ReStartService("server_demo")


        return

    def ReStartService(self,grpc_service_name: str) -> bool:
        # shell命令先删除进程 kill pid
        os.system(f'pgrep -f "python3 /home/lighthouse/test_py/grpc_demo/server/{grpc_service_name}.py" | xargs sudo kill')
        # 重启服务
        os.system(f'python3 /home/lighthouse/test_py/grpc_demo/server/{grpc_service_name}.py >> {self.daemon_log_txt}')
        print(f"重启成功 service_name:{grpc_service_name}")

        return

    def RunHelloClient(self)->bool:
        try:
            with grpc.insecure_channel("localhost:40000") as channel:
                s = hello_pb2_grpc.HelloServiceStub(channel)
                param = hello_pb2.req(user="zoneslee")
                try:
                    resp = s.SayHello(param)
                    print(resp.msg)  # 内容与proto中定义 resp 一致
                except grpc.RpcError as e:
                    print(f"gRPC call failed with error: {e.code()}: {e.details()}")
                    if e.code() == grpc.StatusCode.UNAVAILABLE:
                        print("Server unavailable. Please check if the server is running and reachable.")
                    raise e
                    return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False