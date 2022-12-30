from abc import ABC, abstractmethod


class HandlerUseCase(ABC):
    @abstractmethod
    def execute(self, file_name: str):
        ...


class SmtpMessageContextService(ABC):
    @abstractmethod
    def conn(self, sender: str, password: str):
        ...

    @abstractmethod
    def send(self, receiver: str, message):
        ...


class CsvFileRepository(ABC):
    @abstractmethod
    def account_file(self, account_path: str):
        ...


class TransactionalInformationService(ABC):
    @abstractmethod
    def process_file(self, account_name: str):
        ...

    @abstractmethod
    def get_csv_body_collection(self):
        ...

    @abstractmethod
    def get_csv_monthly_collection(self):
        ...

    @abstractmethod
    def get_credit_average(self):
        ...

    @abstractmethod
    def get_debit_average(self):
        ...

    @abstractmethod
    def get_balance(self):
        ...
