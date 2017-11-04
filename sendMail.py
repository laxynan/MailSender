# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import parseaddr, formataddr
import smtplib
import os.path
import threading
import time

_from_addr = ''
_password = ''
_smtp_server = ''
_to_addr = ''

_title = ''
_content = ''
_attachments = ()

_callback = None

_server = None
_msg = None

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr(( \
        Header(name, 'utf-8').encode(), \
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))

def startSend(from_addr, password, smtp_server, to_addr, title, content, attachments, callback):
    global _from_addr
    global _password
    global _smtp_server
    global _to_addr
    global _title
    global _content
    global _attachments
    global _callback
    _from_addr = from_addr
    _password = password
    _smtp_server = smtp_server
    _to_addr = to_addr
    _title = title
    _content = content
    _attachments = attachments
    _callback = callback
    # sendMail()
    sendThread = threading.Thread(target=sendMail, name='SendmailThread')
    sendThread.start()

def sendMail():
    global _from_addr
    global _password
    global _smtp_server
    global _to_addr
    global _title
    global _content
    global _attachments
    global _callback

    if _callback:
        _callback(0, 0, 0)

    login(_from_addr, _password, _smtp_server)
    assemble(_title, _content, _attachments)
    sendTo(_from_addr, _to_addr, _server, _msg)

    if _callback:
        _callback(1, 1, 0)

    quit(_server)

def login(from_addr, password, smtp_server):
    # global _from_addr
    global _server

    # _from_addr = from_addr

    _server = smtplib.SMTP(smtp_server, 25)
    _server.starttls()
    _server.set_debuglevel(1)
    _server.login(from_addr, password)
    return _server

def assemble(title, content, attachments):
    global _msg

    # 邮件对象:
    _msg = MIMEMultipart()
    _msg['From'] = _format_addr(u'%s' % _from_addr)
    # _msg['To'] = _format_addr(u'%s' % to_addr)
    _msg['Subject'] = Header(title, 'utf-8').encode()

    # 邮件正文是MIMEText:
    _msg.attach(MIMEText(content, 'plain', 'utf-8'))

    for attachment in attachments:
        # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
        with open(attachment, 'rb') as f:
            # 设置附件的MIME和文件名，这里是png类型:
            mime = MIMEBase('application', 'octet-stream')
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment))
            # mime.add_header('Content-ID', '<0>')
            # mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            _msg.attach(mime)
    
    return _msg

def sendTo(from_addr, to_addr, server, msg):
    global _from_addr
    global _server

    if not _server:
        print 'server is None'
        return False
    if not _msg:
        print 'msg is None'
        return False
    _msg['To'] = _format_addr(u'%s' % to_addr)
    _server.sendmail(_from_addr, [to_addr], _msg.as_string())

def quit(server):
    global _server

    if not _server:
        print 'server is None'
        return
    _server.quit()

# server = smtplib.SMTP(smtp_server, 25)
# server.starttls()
# server.set_debuglevel(1)
# server.login(from_addr, password)
# server.sendmail(from_addr, [to_addr], msg.as_string())
# server.quit()

if __name__=='__main__':
    pass