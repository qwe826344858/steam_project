import os
import time
import sys
import grpc
from common_tools.commonConfig import CommonConfig
from grpc_demo.pb import hello_pb2_grpc,hello_pb2

class GrpcSavingDaemon():
    daemon_log_txt = "python_grpc_daemon_stdout.log"
    grpc_host = ""
    grpc_port = 0


    def __init__(self):
        config = CommonConfig.getGrpcConfig()
        self.grpc_host = config["host"]
        self.grpc_port = config["port"]

    def run(self):
        while True:
            self.CheckService()
            time.sleep(1800)
        return

    def CheckService(self):
        # 给grpc服务发送请求
        ret = self.RunHelloClient()
        if ret is False:
            print(f"需要重启 service_name:server_demo")
            self.ReStartService("server_demo")


        return

    def ReStartService(self,grpc_service_name: str) -> bool:
        # shell命令先删除进程 kill pid
        os.system(f'pgrep -f "python3 /home/lighthouse/test_py/grpc_demo/server/{grpc_service_name}.py" | xargs sudo kill')
        # 重启服务
        os.system(f'python3 /home/lighthouse/test_py/grpc_demo/server/{grpc_service_name}.py & >> {self.daemon_log_txt}')
        print(f"重启成功 service_name:{grpc_service_name}")

        return

    def RunHelloClient(self)->bool:
        try:
            with grpc.insecure_channel(f"{self.grpc_host}:{self.grpc_port}") as channel:
                s = hello_pb2_grpc.HelloServiceStub(channel)
                param = hello_pb2.req(user="zoneslee")
                try:
                    resp = s.SayHello(param)
                    print(resp.msg)  # 内容与proto中定义 resp 一致
                except grpc.RpcError as e:
                    print(f"gRPC call failed with error: {e.code()}: {e.details()}")
                    if e.code() == grpc.StatusCode.UNAVAILABLE:
                        print("Server unavailable. Please check if the server is running and reachable.")
                    return False
        except Exception as e:
            print(f"An error occurred: {e}")
            return False



if __name__ == '__main__':
    # 通过命令行输入方法名进行调用
    method_name  = sys.argv[1]     # 获取命令中第一个额外参数
    api = GrpcSavingDaemon()

    # 获取方法对象
    method = getattr(api, method_name, None)

    # 检查方法是否存在
    if method is None or not callable(method):
        print(f"方法 '{method_name}' 不存在或不可调用")
        sys.exit(1)

    # 调用方法
    method()