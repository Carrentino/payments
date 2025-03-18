from decimal import Decimal
from uuid import UUID

from pydantic import ValidationError

from src.db.enums.transaction import TransactionType
from src.db.models.transaction import Transaction
from src.errors.service import InsufficientFundsError
from src.integrations.youkassa import YouKassaClient
from src.repositories.transaction import TransactionRepository
from src.repositories.user_balance import UserBalanceRepository
from src.settings import get_settings
from src.utils import decrypt_data, encrypt_data
from src.web.api.transactions.schemas import (
    DepositOrWithdrawReq,
    DepositOrWithdrawResp,
    TransactionFilters,
    TransactionSchema,
)


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        user_balance_repository: UserBalanceRepository,
        youkassa_client: YouKassaClient,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.user_balance_repository = user_balance_repository
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
        return confirmation_url

    async def process_withdraw(self, data: DepositOrWithdrawReq) -> None:
        if data.card_number is None:
            raise ValidationError
        user_balance = await self.user_balance_repository.get_one_by(user_id=data.user_id)
        if user_balance is None:
            raise InsufficientFundsError
        balance = decrypt_data(user_balance.balance)
        if data.amount > Decimal(balance):
            raise InsufficientFundsError
        await self.youkassa_client.withdraw(data)
        user_balance.balance = encrypt_data(str(Decimal(balance) - data.amount))
        await self.user_balance_repository.update_object(user_balance)

    async def get_transactions(self, user_id: UUID, filters: TransactionFilters) -> tuple[list[TransactionSchema], int]:
        clean_filters = filters.model_dump(mode='python', exclude_none=True)
        transactions, count = await self.transaction_repository.get_paginated_transactions(
            **clean_filters, user_id=user_id
        )
        result = []
        for item in transactions:
            result.append(TransactionSchema.model_validate(item))
        return result, count
