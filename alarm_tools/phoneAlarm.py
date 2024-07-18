import sys
sys.path.append("/home/lighthouse/test_py")
from alarm_tools.commonAlarmHelper import commonAlarmHelper


# TODO 电话告警
class phoneAlarm(commonAlarmHelper):
    def reportMessage(self):
        return