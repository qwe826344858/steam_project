
from common_tools.tools import runDaemon
from common_tools.loggerHelper import Logger


# 初始化日志
Logger.init()
class VisualGraphics:
    def testlog(self):
        Logger.info("新增测试")


if __name__ == '__main__':
    runDaemon(api=VisualGraphics())
