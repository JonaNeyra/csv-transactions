import csv
from ...model.contracts import CsvFileRepository


class AccountCsvFileRepository(CsvFileRepository):
    path_origin: str = "transactions/"
    input_file_extension: str = "csv"

    def account_file(self, account_name: str):
        account_path = "{origin}{account}.{ext}".format(
            origin=self.path_origin,
            account=account_name,
            ext=self.input_file_extension
        )
        csv_file = open(account_path, 'r')
        account_csv = csv.reader(csv_file, delimiter=',')

        return account_csv
