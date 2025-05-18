from uuid import uuid4, UUID

from helpers.clients.http_client import BaseApiClient
from helpers.errors.api import ValidationError
from yookassa import Configuration, Payout
from yookassa import Payment

from src.integrations.schemas.youkassa import (
    Amount,
    CreatePaymentSchema,
    Confirmation,
    PaymentMethodData,
    PayoutSchema,
    PayoutDestinationDataSchema,
    CardSchema,
    PayMeta,
)
from src.settings import get_settings
from src.web.api.transactions.schemas import DepositOrWithdrawReq


class YouKassaClient(BaseApiClient):
    _base_url = get_settings().youkassa.url

    def __init__(self):
        Configuration.account_id = get_settings().youkassa.account_id.get_secret_value()
        Configuration.secret_key = get_settings().youkassa.api_key.get_secret_value()
        super().__init__()

    async def deposit(self, data: DepositOrWithdrawReq, tr_id: UUID) -> str:
        idempotence_key = str(uuid4())
        payment = CreatePaymentSchema(
            amount=Amount(value=data.amount),
            payment_method_data=PaymentMethodData(type='bank_card'),
            confirmation=Confirmation(return_url=data.payment_redirect),
            description=data.description,
            metadata=PayMeta(transaction_id=tr_id),
        )
        created_payment = Payment.create(payment.model_dump(mode='python'), idempotence_key)

        confirmation_url = created_payment.confirmation.confirmation_url
        return confirmation_url

    async def withdraw(self, data: DepositOrWithdrawReq, tr_id: UUID) -> None:
        idempotence_key = str(uuid4())
        payout = PayoutSchema(
            amount=Amount(value=data.amount),
            payout_destination_data=PayoutDestinationDataSchema(
                card=CardSchema(
                    number=data.card_number,
                )
            ),
            description=data.description,
            metadata=PayMeta(transaction_id=tr_id),
        )
        try:
            Payout.create(payout.model_dump(mode='python'), idempotence_key)
        except ValueError as e:
            raise ValidationError(str(e)) from None
