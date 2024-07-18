import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys
sys.path.append("/home/lighthouse/test_py")
from common_tools.commonConfig import CommonConfig
from common_tools.loggerHelper import Logger

# 初始化日志
Logger.init()

# 邮件
class mailHelper:

    def __init__(self):
        commonConfig = CommonConfig()
        self.mailConfig = commonConfig.getMailConfig()
        self.sender_email = list(self.mailConfig['sender_email_config'].keys())[0]
        self.password = list(self.mailConfig['sender_email_config'].values())[0]
        self.recipient_emails = self.mailConfig['recipient_mail_list']



    def sendMail(self,subject,body):
        # 邮件配置
        Logger.info(f"邮件配置 config:{self.mailConfig} 主题:{subject} 内容:{body}")

        # 创建一个MIMEMultipart对象
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = ", ".join(self.recipient_emails)
        message["Subject"] = subject

        # 将内容添加到邮件正文
        message.attach(MIMEText(body, "plain"))

        # 发送邮件
        try:
            smtp_obj = smtplib.SMTP("smtp.gmail.com", 587)
            smtp_obj.starttls()
            smtp_obj.login(self.sender_email, self.password)  # 这里填写你的邮箱密码
            smtp_obj.sendmail(self.sender_email, self.recipient_emails, message.as_string())
            smtp_obj.quit()
        except smtplib.SMTPException:
            Logger.info(f"发送邮件失败! message:{message}")
            return False

        return True


if __name__ == '__main__':
    mail = mailHelper()
    mail.sendMail()