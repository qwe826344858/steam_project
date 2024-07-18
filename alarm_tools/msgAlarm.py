import sys
sys.path.append("/home/lighthouse/test_py")
from alarm_tools.commonAlarmHelper import commonAlarmHelper


# TODO 短信告警
class msgAlarm(commonAlarmHelper):
    def reportMessage(self):
        return