from typing import List
from collections.abc import Iterable, Iterator

from ...model.dtos import CsvRow


class TransversalAccountTransactions(Iterator):
    _position = None
    _reverse: bool = False

    def __init__(self, transaction_collection, reverse: bool = False) -> None:
        self.transaction_collection = transaction_collection
        self._reverse = reverse
        self._position = -1 if reverse else 0

    def __next__(self):
        try:
            value = self.transaction_collection[self._position]
            self._position += -1 if self._reverse else 1
        except IndexError:
            raise StopIteration()

        return value


class TransactionalBody(Iterable):
    def __init__(self, transaction_collection: List[CsvRow] = []):
        self.transaction_collection = transaction_collection

    def __iter__(self) -> TransversalAccountTransactions:
        return TransversalAccountTransactions(self.transaction_collection)

    def get_reverse(self) -> TransversalAccountTransactions:
        return TransversalAccountTransactions(self.transaction_collection, True)

    def add_row(self, item: dict):
        csv_row = CsvRow(**item)
        self.transaction_collection.append(csv_row)
