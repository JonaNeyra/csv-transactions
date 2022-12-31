import os
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

from ..model.catalogs import Months
from ..model.contracts import HandlerUseCase, TransactionalInformationService, SmtpMessageContextService
from ..web.templates.stori_mail import balance_html


class NotifyTransactionReport(HandlerUseCase):
    stori_logo_name: str = "stori-logo.png"

    def __init__(
        self,
        account_info_service: TransactionalInformationService,
        mail_service: SmtpMessageContextService
    ):
        self.path_origin = f"{os.path.dirname(__file__)}/../data/"
        self.account_info_service = account_info_service
        self.mail_service = mail_service
        self.file_name = ""

    def execute(self, file_name: str):
        if file_name == "":
            raise ValueError("Without UUID")

        mail_from = os.environ['SENDER_MAIL']
        mail_to = os.environ['RECEIVER_MAIL']
        sender_pass = os.environ['SENDER_PASS']
        self.file_name = file_name
        self.account_info_service.process_file(self.file_name)
        message_to_send = self.__create_message(mail_from, mail_to)
        self.mail_service.conn(mail_from, sender_pass)
        self.mail_service.send(mail_to, message_to_send)

    def __create_message(self, mail_from: str, mail_to: str):
        message = MIMEMultipart("mixed")
        message["Subject"] = "Stori's Balance Report"
        message["From"] = mail_from
        message["To"] = mail_to

        image_part = self.__mail_logo()
        html_part = self.__mail_body()
        attach_part = self.__mail_attachment()

        message.attach(html_part)
        message.attach(image_part)
        message.attach(attach_part)

        return message

    def __mail_body(self):
        operations_by_month = self.__monthly_sentences()
        html_body = balance_html.format(
            balance=self.account_info_service.get_balance(),
            monthly_transactions=operations_by_month,
            debit_average=self.account_info_service.get_debit_average(),
            credit_average=self.account_info_service.get_credit_average()
        )
        html_part = MIMEText(html_body, "html")
        return html_part

    def __mail_logo(self):
        binary_image = open(f"{self.path_origin}static/{self.stori_logo_name}", 'rb')
        image_part = MIMEImage(binary_image.read())
        binary_image.close()
        image_part.add_header('Content-Id', '<stori_cid_png>')
        return image_part

    def __mail_attachment(self):
        full_file_name = f"{self.file_name}.csv"
        binary_attach = open(f"{self.path_origin}{full_file_name}", 'rb')
        attach_part = MIMEApplication(binary_attach.read(), Name=full_file_name)
        binary_attach.close()
        return attach_part

    def __monthly_sentences(self):
        monthly_collection = self.account_info_service.get_csv_monthly_collection()
        operations_by_month = ""
        for month, operations in monthly_collection.items():
            sentence = "&nbsp;&nbsp;&nbsp;&nbsp;Number of transactions in {month}: {operations}<br>".format(
                month=Months(int(month)).name.capitalize(),
                operations=len(operations)
            )

            operations_by_month = operations_by_month + sentence
        return operations_by_month

