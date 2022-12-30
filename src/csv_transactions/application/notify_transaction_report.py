import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from ..model.catalogs import Months
from ..model.contracts import HandlerUseCase, TransactionalInformationService, SmtpMessageContextService
from ..web.templates.stori_mail import balance_html


class NotifyTransactionReport(HandlerUseCase):
    def __init__(
        self,
        account_info_service: TransactionalInformationService,
        mail_service: SmtpMessageContextService
    ):
        self.account_info_service = account_info_service
        self.mail_service = mail_service

    def execute(self, file_name: str):
        if file_name == "":
            raise ValueError("Without UUID")

        mail_from = os.environ['SENDER_MAIL']
        mail_to = os.environ['RECEIVER_MAIL']
        sender_pass = os.environ['SENDER_PASS']
        self.account_info_service.process_file(file_name)
        message_to_send = self.__create_message(mail_from, mail_to)
        self.mail_service.conn(mail_from, sender_pass)
        self.mail_service.send(mail_to, message_to_send)

    def __create_message(self, mail_from: str, mail_to: str):
        message = MIMEMultipart("alternative")
        message["Subject"] = "Stori's Balance Report"
        message["From"] = mail_from
        message["To"] = mail_to

        monthly_collection = self.account_info_service.get_csv_monthly_collection()
        operations_by_month = ""
        for month, operations in monthly_collection.items():
            sentence = "&nbsp;&nbsp;&nbsp;&nbsp;Number of transactions in {month}: {operations}<br>".format(
                month=Months(int(month)).name,
                operations=len(operations)
            )

            operations_by_month = operations_by_month + sentence

        html_body = balance_html.format(
            balance=self.account_info_service.get_balance(),
            monthly_transactions=operations_by_month,
            debit_average=self.account_info_service.get_debit_average(),
            credit_average=self.account_info_service.get_credit_average()
        )

        html_part = MIMEText(html_body, "html")
        message.attach(html_part)

        return message

