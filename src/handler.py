from typing import Any

from src.csv_transactions import (
    AccountTransactionalInformation,
    AccountCsvFileRepository
)


def handle(event: dict, context: Any):
    account_transactional_info = AccountTransactionalInformation(
        AccountCsvFileRepository()
    )
    account_transactional_info.process_file('3dbc158a-4856-45c8-a329-fb26f7f9ec19')
    collection = account_transactional_info.get_balance()

    print(collection)
    print("Event: ", event)
    print("Context: ", context)
    return "Hello Docker RIE"
