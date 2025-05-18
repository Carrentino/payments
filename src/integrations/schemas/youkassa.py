from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel

from src.settings import get_settings


class Amount(BaseModel):
    value: Decimal
    currency: str = 'RUB'


class PaymentMethodData(BaseModel):
    type: str = 'bank_card'


class Confirmation(BaseModel):
    type: str = 'redirect'
    return_url: str = get_settings().payment_redirect


class PayMeta(BaseModel):
    transaction_id: UUID


class CreatePaymentSchema(BaseModel):
    amount: Amount
    payment_method_data: PaymentMethodData
    confirmation: Confirmation
    description: str | None = None
    metadata: PayMeta


class CardSchema(BaseModel):
    number: str


class PayoutDestinationDataSchema(BaseModel):
    type: str = 'bank_card'
    card: CardSchema


class PayoutSchema(BaseModel):
    amount: Amount
    payout_destination_data: PayoutDestinationDataSchema
    description: str
    metadata: PayMeta
