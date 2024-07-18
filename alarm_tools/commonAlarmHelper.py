

# 标识位 用户判断组合告警
ALARM_MAIL = 1      # 邮件告警
ALARM_PHONE = 2     # 电话告警
ALARM_SOFTWARE = 4  # 通讯软件告警
ALARM_MSG = 8       # 短信告警

class commonAlarmHelper:
    alarm_type = ALARM_MAIL        # 告警等级默认选择邮件告警

    # alarm_type = ALARM_MAIL | ALARM_PHONE | ALARM_SOFTWARE | ALARM_MSG
    def __init__(self,alarm_type):
        if alarm_type > 0:
            self.alarm_level = alarm_type



    def reportMessage(self):
        return




if __name__ == '__main__':
    a = ALARM_MAIL | ALARM_PHONE | ALARM_SOFTWARE | ALARM_MSG
    print(a)