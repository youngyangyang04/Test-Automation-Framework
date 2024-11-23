import smtplib
from email.mime.text import MIMEText
from conf.operationConfig import OperationConfig
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication  # 附件
from conf import setting
from common.recordlog import logs
import re

conf = OperationConfig()


class SendEmail(object):
    """构建邮件主题、正文、附件"""

    def __init__(
            self,
            host=conf.get_section_for_data('EMAIL', 'host'),
            user=conf.get_section_for_data('EMAIL', 'user'),
            passwd=conf.get_section_for_data('EMAIL', 'passwd')):
        self.__host = host
        self.__user = user
        self.__passwd = passwd

    def build_content(self, subject, email_content, addressee=None, atta_file=None):
        """
        构建邮件格式，邮件正文、附件
        @param subject: 邮件主题
        @param addressee: 收件人，在配置文件中以;分割
        @param email_content: 邮件正文内容
        @return:
        """
        user = 'liaison officer' + '<' + self.__user + '>'
        # 收件人
        if addressee is None:
            addressee = conf.get_section_for_data('EMAIL', 'addressee').split(';')
        else:
            addressee = addressee.split(';')
        message = MIMEMultipart()
        message['Subject'] = subject
        message['From'] = user
        message['To'] = ';'.join([re.search(r'(.*)(@)', emi).group(1) + "<" + emi + ">" for emi in addressee])

        # 邮件正文
        text = MIMEText(email_content, _subtype='plain', _charset='utf-8')
        message.attach(text)

        if atta_file is not None:
            # 附件
            atta = MIMEApplication(open(atta_file, 'rb').read())
            atta['Content-Type'] = 'application/octet-stream'
            atta['Content-Disposition'] = 'attachment; filename="testresult.xls"'
            message.attach(atta)

        try:
            service = smtplib.SMTP_SSL(self.__host)
            service.login(self.__user, self.__passwd)
            service.sendmail(user, addressee, message.as_string())
        except smtplib.SMTPConnectError as e:
            logs.error('邮箱服务器连接失败！', e)
        except smtplib.SMTPAuthenticationError as e:
            logs.error('邮箱服务器认证错误,POP3/SMTP服务未开启,密码应填写授权码!', e)
        except smtplib.SMTPSenderRefused as e:
            logs.error('发件人地址未经验证！', e)
        except smtplib.SMTPDataError as e:
            logs.error('发送的邮件内容包含了未被许可的信息，或被系统识别为垃圾邮件！', e)
        except Exception as e:
            logs.error(e)
        else:
            logs.info('邮件发送成功!')
            service.quit()


class BuildEmail(SendEmail):
    """发送邮件"""

    # def __int__(self, host, user, passwd):
    #     super(BuildEmail, self).__init__(host, user, passwd)

    def main(self, success, failed, error, not_running, atta_file=None, *args):
        """
        :param success: list类型
        :param failed: list类型
        :param error: list类型
        :param not_running: list类型
        :param atta_file: 附件路径
        :param args:
        :return:
        """
        success_num = len(success)
        fail_num = len(failed)
        error_num = len(error)
        notrun_num = len(not_running)
        total = success_num + fail_num + error_num + notrun_num
        execute_case = success_num + fail_num
        pass_result = "%.2f%%" % (success_num / execute_case * 100)
        fail_result = "%.2f%%" % (fail_num / execute_case * 100)
        err_result = "%.2f%%" % (error_num / execute_case * 100)
        # 设置邮件主题、收件人、内容
        subject = conf.get_section_for_data('EMAIL', 'subject')
        addressee = conf.get_section_for_data('EMAIL', 'addressee').split(';')
        content = "     ***项目接口测试，共测试接口%s个，通过%s个，失败%s个，错误%s个，未执行%s个，通过率%s，失败率%s，错误率%s。" \
                  "详细测试结果请参见附件。" % (
                      total, success_num, fail_num, error_num, notrun_num, pass_result, fail_result, err_result)
        self.build_content(addressee, subject, content, atta_file)
