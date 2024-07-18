import sys
sys.path.append("/home/lighthouse/test_py")
from alarm_tools.commonAlarmHelper import commonAlarmHelper


# TODO 通讯软件告警
class softwareAlarm(commonAlarmHelper):
    def reportMessage(self):
        return