from typing import Any

from src.csv_transactions import (
    AccountTransactionalInformation,
    AccountCsvFileRepository,
    NotifyTransactionReport,
    SmtpMessageContext
)


def handle(event: dict, context: Any):
    print("Event: ", event)
    print("Context: ", context)

    if "operation" in event and event["operation"] == "BALANCE_REPORT":
        account_transactional_info = AccountTransactionalInformation(AccountCsvFileRepository())
        smtp_mailer = SmtpMessageContext()
        transaction_report = NotifyTransactionReport(
            account_info_service=account_transactional_info,
            mail_service=smtp_mailer
        )

        transaction_report.execute(event.get("user_uuid", ""))
    else:
        raise NotImplementedError("The operation is not implemented.")

    return "The message has been sent."
