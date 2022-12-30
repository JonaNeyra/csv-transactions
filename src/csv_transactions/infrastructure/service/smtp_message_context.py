import smtplib
import ssl
from ...model.contracts import SmtpMessageContextService


class SmtpMessageContext(SmtpMessageContextService):
    smtp_host = "smtp.gmail.com"
    smtp_port = 465

    def __init__(self):
        self.context = ssl.create_default_context()
        self.server = None
        self.sender = ""

    def conn(self, sender: str, password: str):
        self.sender = sender
        self.server = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port, context=self.context)
        self.server.login(self.sender, password)

    def send(self, receiver: str, message):
        self.server.sendmail(self.sender, receiver, message.as_string())
