import csv
import os.path

from ...model.contracts import CsvFileRepository


class AccountCsvFileRepository(CsvFileRepository):
    input_file_extension: str = "csv"

    def __init__(self):
        self.path_origin = f"{os.path.dirname(__file__)}/../../data/"

    def account_file(self, account_name: str):
        account_path = "{origin}{account}.{ext}".format(
            origin=self.path_origin,
            account=account_name,
            ext=self.input_file_extension
        )

        print("Path: ", account_path)

        csv_file = open(account_path, 'r')
        account_csv = csv.reader(csv_file, delimiter=',')

        return account_csv
