import sys
sys.path.append("/home/lighthouse/test_py")
from alarm_tools.commonAlarmHelper import commonAlarmHelper


# TODO 邮件告警
class mailAlarm(commonAlarmHelper):
    def reportMessage(self):
        return