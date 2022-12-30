from ..model.contracts import HandlerUseCase, TransactionalInformationService


class NotifyTransactionReport(HandlerUseCase):
    def __init__(self, account_info_service: TransactionalInformationService):
        self.account_info_service = account_info_service

    def execute(self, file_name: str):
        ...
