from src.db.enums.transaction import TransactionType
from src.db.models.transaction import Transaction
from src.integrations.youkassa import YouKassaClient
from src.repositories.transaction import TransactionRepository
from src.settings import get_settings
from src.web.api.transactions.schemas import DepositOrWithdrawReq, DepositOrWithdrawResp


class TransactionService:
    def __init__(self, transaction_repository: TransactionRepository, youkassa_client: YouKassaClient) -> None:
        self.transaction_repository = transaction_repository
        self.youkassa_client = youkassa_client

    async def process_transaction(self, data: DepositOrWithdrawReq) -> DepositOrWithdrawResp:
        if data.transaction_type == TransactionType.DEPOSIT:
            confirmation_url = await self.process_deposit(data)
        else:
            confirmation_url = await self.process_withdraw(data)

        transaction = Transaction(
            user_id=data.user_id,
            amount=data.amount,
            transaction_type=data.transaction_type,
            payment_redirect=data.payment_redirect if data.payment_redirect else get_settings().payment_redirect,
            confirmation_url=confirmation_url,
        )
        await self.transaction_repository.create(transaction)
        return DepositOrWithdrawResp(confirmation_url=confirmation_url)

    async def process_deposit(self, data: DepositOrWithdrawReq) -> str:
        confirmation_url = await self.youkassa_client.deposit(data)
        transaction = Transaction(
            user_id=data.user_id,
            amount=data.amount,
            transaction_type=data.transaction_type,
            payment_redirect=data.payment_redirect if data.payment_redirect else get_settings().payment_redirect,
            confirmation_url=confirmation_url,
        )
        await self.transaction_repository.create(transaction)
        return confirmation_url

    async def process_withdraw(self, data: DepositOrWithdrawReq):
        pass
