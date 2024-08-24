import os

class GrpcSavingDaemon():
    def run(self):
        return

    def CheckService(self):
        # 给grpc服务发送请求
        return

    def ReStartService(self,grpc_name: str) -> bool:
        # shell命令先删除进程 kill pid
        os.system('pgrep -f "/home/lighthouse/clash/clash-linux-amd64-v3-v1.18.0" | xargs sudo kill')

        # 重启服务

        return

