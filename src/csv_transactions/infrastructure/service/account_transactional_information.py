from __future__ import annotations
from datetime import datetime

from ..service.account_iterable import TransactionalBody
from ...model.contracts import TransactionalInformationService, CsvFileRepository


class AccountTransactionalInformation(TransactionalInformationService):

    def __init__(self, csv_file_repository: CsvFileRepository, account: str = ""):
        self.account = account
        self.csv_file_repository = csv_file_repository
        self.transaction_collection = None
        self.monthly_transactions = {}
        self.credit_transactions = []
        self.debit_transactions = []
        self.balance = 0

    def process_file(self, account_name: str):
        self.account = account_name
        account_csv = self.csv_file_repository.account_file(self.account)
        self.__collections_allocation(account_csv)

    def get_csv_body_collection(self):
        return self.transaction_collection

    def get_csv_monthly_collection(self):
        return self.monthly_transactions

    def get_credit_average(self):
        return sum(self.credit_transactions) / len(self.credit_transactions)

    def get_debit_average(self):
        return sum(self.debit_transactions) / len(self.debit_transactions)

    def get_balance(self):
        return self.balance

    def __collections_allocation(self, account_csv):
        if self.account == "":
            raise ValueError("No fue proporcionado una cuenta correcta")

        now = datetime.now()
        self.transaction_collection = TransactionalBody()
        for row_index, row in enumerate(account_csv):
            if row_index < 1 or len(row) != 3:
                continue

            transaction_id = int(row[0])
            transaction_value = float(row[2])
            transaction_date = datetime.strptime(
                f"{row[1]}/{now.year}",
                '%m/%d/%Y'
            )

            transaction_body = {
                "id": transaction_id,
                "date": transaction_date,
                "transaction": transaction_value
            }

            if self.transaction_collection is not None:
                self.__add_to_collection(transaction_body)

            month_val = transaction_date.month
            month_eval = month_val in self.monthly_transactions

            if not month_eval:
                self.monthly_transactions[month_val] = []
                self.monthly_transactions[month_val].append(transaction_body)
            else:
                self.monthly_transactions[month_val].append(transaction_body)

            if transaction_value >= 0:
                self.credit_transactions.append(transaction_value)

            if transaction_value < 0:
                self.debit_transactions.append(transaction_value)

            self.balance = self.balance + transaction_value

    def __add_to_collection(self, transaction: dict):
        self.transaction_collection.add_row(transaction)
