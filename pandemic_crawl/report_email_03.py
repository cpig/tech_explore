import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import datetime

MAIL_HOST = 'smtp.163.com'
MAIL_USER = 'c_pig8828'
MAIL_PSWD = 'hjyhjdzwxq'
SENDER = 'c_pig8828@163.com'
RECEIVERS = ['c_pig8828@163.com','Xi.Liu0@walmart.com','Stella.Guo@walmart.com']

today_str = datetime.datetime.strftime(datetime.datetime.now(),"%Y%m%d")
#html_doc= get_html_base64()
message = MIMEMultipart()
message['Subject'] = '重点城市疫情信息-%s'%today_str
message['From'] = SENDER
message['To'] = ';'.join(RECEIVERS)

mime_html = MIMEText(open("output.htm","r",encoding="utf8").read(), 'html', 'utf-8')
message.attach(mime_html)
#mime_report = MIMEText(open("output.htm","r").read(), 'html', 'utf-8')
#mime_report.add_header('Content-Type', 'application/html')

#mime_report.add_header('Content-Disposition', 'attachment', filename="IKEA周销榜-%s.html"%today_str)
#message.attach(mime_report)
'''pic_cnt = 0
for pic in pic_list:
    mime_pic = MIMEImage(open("pic/"+pic,"rb").read())
    mime_pic['Content-Type'] = 'application/octet-stream'
    mime_pic['Content-Disposition'] = 'attachment;filename="%s"'%pic
    message.attach(mime_pic)
    pic_cnt+=1
    if(pic_cnt%10==0):
        print(pic_cnt)'''

smtp = smtplib.SMTP()
smtp.connect(MAIL_HOST, 25)
smtp.login(MAIL_USER, MAIL_PSWD)
smtp.sendmail(SENDER, RECEIVERS, message.as_string())
smtp.quit()

