from decimal import Decimal
from uuid import UUID, uuid4

from pydantic import ValidationError

from src.db.enums.transaction import TransactionType, TransactionStatus
from src.db.models.transaction import Transaction
from src.db.models.user_balance import UserBalance
from src.errors.service import InsufficientFundsError, TransactionNotFoundError
from src.integrations.schemas.users import UpdateBalanceMessage, UpdateBalance
from src.integrations.users import UsersClient
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
    ReserveReq,
    SubmitTransactionReq,
)

YOUKASSA_ST = {'payment.succeeded': TransactionStatus.SUCCESS, 'payment.canceled': TransactionStatus.CANCELLED}


class TransactionService:
    def __init__(
        self,
        transaction_repository: TransactionRepository,
        user_balance_repository: UserBalanceRepository,
        youkassa_client: YouKassaClient,
        users_client: UsersClient,
    ) -> None:
        self.transaction_repository = transaction_repository
        self.user_balance_repository = user_balance_repository
        self.youkassa_client = youkassa_client
        self.users_client = users_client

    async def process_transaction(self, data: DepositOrWithdrawReq) -> DepositOrWithdrawResp:
        tr_id = uuid4()
        if data.transaction_type == TransactionType.DEPOSIT:
            confirmation_url = await self.process_deposit(data, tr_id)
        else:
            confirmation_url = await self.process_withdraw(data, tr_id)

        transaction = Transaction(
            id=tr_id,
            user_id=data.user_id,
            amount=data.amount,
            transaction_type=data.transaction_type,
            payment_redirect=data.payment_redirect if data.payment_redirect else get_settings().payment_redirect,
            confirmation_url=confirmation_url,
        )
        await self.transaction_repository.create(transaction)
        return DepositOrWithdrawResp(confirmation_url=confirmation_url)

    async def process_deposit(self, data: DepositOrWithdrawReq, tr_id: UUID) -> str:
        confirmation_url = await self.youkassa_client.deposit(data, tr_id)
        return confirmation_url

    async def process_withdraw(self, data: DepositOrWithdrawReq, tr_id: UUID) -> None:
        if data.card_number is None:
            raise ValidationError
        user_balance = await self.user_balance_repository.get_one_by(user_id=data.user_id)
        if user_balance is None:
            raise InsufficientFundsError
        balance = decrypt_data(user_balance.balance)
        if data.amount > Decimal(balance):
            raise InsufficientFundsError
        await self.youkassa_client.withdraw(data, tr_id)
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

    async def reserve(self, data: ReserveReq) -> UUID:
        user_balance = await self.user_balance_repository.get_one_by(user_id=data.user_from)
        if user_balance is None:
            raise InsufficientFundsError
        balance = decrypt_data(user_balance.balance)
        if data.amount < Decimal(balance):
            raise InsufficientFundsError
        new_balance = Decimal(balance) - data.amount
        user_balance.balance = encrypt_data(str(new_balance))
        await self.user_balance_repository.update_object(user_balance)
        transaction = Transaction(
            user_id=data.user_from,
            amount=data.amount,
            transaction_type=TransactionType.TRANSFER,
            status=TransactionStatus.RESERVED,
            payment_redirect="",
            confirmation_url=str(data.user_to),
        )
        tr = await self.transaction_repository.create(transaction)
        message = UpdateBalanceMessage(balances=[UpdateBalance(user_id=data.user_from, balance=new_balance)])
        await self.users_client.send_balance(message)
        return tr

    async def submit(self, data: SubmitTransactionReq):
        tr = await self.transaction_repository.get(data.transaction_id)
        if tr is None:
            raise TransactionNotFoundError
        user_to = UUID(tr.confirmation_url)
        user_balance = await self.user_balance_repository.get_one_by(user_id=user_to)
        if user_balance is None:
            user_balance = UserBalance(
                user_id=user_to,
                balance=encrypt_data(str(tr.amount)),
            )
            await self.user_balance_repository.create(user_balance)

            message = UpdateBalanceMessage(
                balances=[
                    UpdateBalance(
                        user_id=user_to,
                        balance=tr.amount,
                    )
                ]
            )
            await self.users_client.send_balance(message)
            return
        balance = Decimal(decrypt_data(user_balance.balance)) + tr.amount
        user_balance.balance = encrypt_data(str(balance))
        await self.user_balance_repository.update_object(user_balance)

        message = UpdateBalanceMessage(balances=[UpdateBalance(user_id=user_to, balance=balance)])
        await self.users_client.send_balance(message)

    async def process_webhook(self, data: dict):
        if data.get('event') not in YOUKASSA_ST:
            return
        new_status = YOUKASSA_ST.get(data.get('event'))
        tr_id = data['object']['metadata'].get('transaction_id')
        if tr_id is None:
            return
        tr = await self.transaction_repository.get(tr_id)
        if tr is None:
            raise TransactionNotFoundError
        tr.status = new_status
        await self.transaction_repository.update_object(tr)
        if new_status != TransactionStatus.SUCCESS:
            return
        user_balance = await self.user_balance_repository.get_one_by(user_id=tr.user_id)
        if user_balance is None:
            user_balance = UserBalance(
                user_id=tr.user_id,
                balance=encrypt_data(str(tr.amount)),
            )
            await self.user_balance_repository.create(user_balance)
            message = UpdateBalanceMessage(
                balances=[
                    UpdateBalance(
                        user_id=tr.user_id,
                        balance=encrypt_data(str(tr.amount)),
                    )
                ]
            )
            await self.users_client.send_balance(message)
            return
        balance = Decimal(decrypt_data(user_balance.balance)) + tr.amount
        user_balance.balance = encrypt_data(str(balance))
        await self.user_balance_repository.update_object(user_balance)

        message = UpdateBalanceMessage(balances=[UpdateBalance(user_id=tr.user_id, balance=balance)])
        await self.users_client.send_balance(message)
