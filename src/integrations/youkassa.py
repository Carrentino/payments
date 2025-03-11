from uuid import uuid4

from helpers.clients.http_client import BaseApiClient
from yookassa import Configuration
from yookassa import Payment

from src.integrations.schemas.youkassa import Amount, CreatePaymentSchema, Confirmation, PaymentMethodData
from src.settings import get_settings
from src.web.api.transactions.schemas import DepositOrWithdrawReq


class YouKassaClient(BaseApiClient):
    _base_url = get_settings().youkassa.url

    def __init__(self):
        Configuration.account_id = get_settings().youkassa.account_id.get_secret_value()
        Configuration.secret_key = get_settings().youkassa.api_key.get_secret_value()
        super().__init__()

    async def deposit(self, data: DepositOrWithdrawReq) -> str:
        idempotence_key = str(uuid4())
        payment = CreatePaymentSchema(
            amount=Amount(value=data.amount),
            payment_method_data=PaymentMethodData(type='bank_card'),
            confirmation=Confirmation(return_url=data.payment_redirect),
            description=data.description,
        )
        created_payment = Payment.create(payment.model_dump(mode='python'), idempotence_key)

        confirmation_url = created_payment.confirmation.confirmation_url
        return confirmation_url
