#!/usr/bin/env python
# -*- coding: utf-8 -*-
# created: zhangpeng <zhangpeng1@infohold.com.cn>


import smtplib
from scloud.config import logger
from scloud.celeryapp import celery
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@celery.task
def sendMail(FROM,TO,SUBJECT,CONTENT,SERVER="smtp.infohold.com.cn"):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = SUBJECT
    msg['From'] = FROM
    msg['To'] = ", ".join(TO)
#     html = """\
# <html>
#   <head></head>
#   <body>
#     <p>Hi!<br>
#        How are you?<br>
#        Here is the <a href="https://www.python.org">link</a> you wanted.
#     </p>
#   </body>
# </html>
# """
    part1 = MIMEText(CONTENT.encode("utf-8"), 'html', 'utf-8')
    msg["Accept-Language"] = "zh-CN"
    msg["Accept-Charset"] = "ISO-8859-1,utf-8"
    msg.attach(part1)
    # Send the mail
    server = smtplib.SMTP(SERVER, 25)
    server.login(FROM, "infohold.com")
    server.sendmail(FROM, TO, msg.as_string())
    server.quit()


if __name__ == '__main__':
    sendMail.delay("scloud@infohold.com.cn", ["zhangpeng820213@gmail.com"], "foo test", "\ncontent1")
