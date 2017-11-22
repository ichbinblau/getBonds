#!/usr/bin/python
# -*- coding: UTF-8 -*-

import requests
import datetime
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import sys
reload(sys)
sys.setdefaultencoding('utf8')

url = "http://dcfm.eastmoney.com/em_mutisvcexpandinterface/api/js/get?type=KZZ_LB&token=70f12f2f4f091e459a279469fe49eca5"
http_proxy  = "http://proxy-shm.intel.com:911"
https_proxy = "https://proxy-shm.intel.com:911"

proxyDict = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
            }

r = requests.get(url, proxies=proxyDict)
r.raise_for_status()

today = (datetime.datetime.now().date() + datetime.timedelta(days=2)).strftime('%Y-%m-%d')

output = "今天是 {}\n今日可申购可转债: \n".format(today)
for r in r.json():
    name, date, code = r.get("SNAME"), r.get("STARTDATE"), r.get("CORRESCODE")
    if today in date:
        output += ",".join((name, date, code))
        output += "\n"

host_server = 'smtp.qq.com'
sender_qq = '42397657'
pwd = 'Cde3$rfv'
sender_qq_mail = '42397657@qq.com'
receiver = 'ichbinblau.3@foxmail.com'
mail_content = output
mail_title = u"今日可转债"

#ssl login
smtp = SMTP_SSL(host_server)
smtp.set_debuglevel(1)
smtp.ehlo(host_server)
smtp.login(sender_qq, pwd)

msg = MIMEText(mail_content, "plain", 'utf-8')
msg["Subject"] = Header(mail_title, 'utf-8')
msg["From"] = sender_qq_mail
msg["To"] = receiver
smtp.sendmail(sender_qq_mail, receiver, msg.as_string())
smtp.quit()
