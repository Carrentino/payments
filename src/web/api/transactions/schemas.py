from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.db.enums.transaction import TransactionType


class DepositOrWithdrawReq(BaseModel):
    user_id: UUID
    amount: Decimal
    transaction_type: TransactionType
    payment_redirect: str | None = None
    description: str | None = None
    card_number: str | None = None


class DepositOrWithdrawResp(BaseModel):
    confirmation_url: str | None = None
