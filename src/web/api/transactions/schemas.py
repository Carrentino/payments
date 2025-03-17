from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.db.enums.transaction import TransactionType, TransactionStatus


class DepositOrWithdrawReq(BaseModel):
    user_id: UUID
    amount: Decimal
    transaction_type: TransactionType
    payment_redirect: str | None = None
    description: str | None = None
    card_number: str | None = None


class DepositOrWithdrawResp(BaseModel):
    confirmation_url: str | None = None


class TransactionFilters(BaseModel):
    transaction_type: TransactionType | None = None
    status: TransactionStatus | None = None

    offset: int = 0
    limit: int = 30


class TransactionSchema(BaseModel):
    user_id: UUID
    amount: Decimal
    transaction_type: TransactionType
    status: TransactionStatus

    class Config:
        from_attributes = True
