from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
import smtplib


class MailClient:
    def __init__(self, server, port, username, password, send_from, subject):
        self.server = server
        self.username = username
        self.password = password
        self.send_from = send_from
        self.subject = subject

    def send_files(self, to, files):
        server = smtplib.SMTP(self.server, 587)
        server.starttls()
        server.login(self.username, self.password)
        msg = MIMEMultipart()
        msg["From"] = self.send_from
        msg["To"] = to
        msg["Date"] = formatdate(localtime=True)
        msg["Subject"] = self.subject
        for file in files:
            part = MIMEApplication(file["content"], Name=file["name"])
            part["Content-Disposition"] = 'attachment; filename="%s"' % file["name"]
            msg.attach(part)
        server.sendmail(self.send_from, to, msg.as_string())
        server.close()
