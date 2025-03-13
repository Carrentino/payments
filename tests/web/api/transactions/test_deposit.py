from decimal import Decimal
from unittest.mock import patch, AsyncMock
from uuid import uuid4

from httpx import AsyncClient
from starlette import status

from src.db.enums.transaction import TransactionType
from src.web.api.transactions.schemas import DepositOrWithdrawReq


@patch('src.integrations.youkassa.YouKassaClient.deposit', new_callable=AsyncMock)
async def test_deposit(mock_deposit: AsyncMock, client: AsyncClient) -> None:
    req = DepositOrWithdrawReq(
        user_id=uuid4(),
        amount=Decimal(10.10),
        transaction_type=TransactionType.DEPOSIT,
    )
    conf_url = 'https://test/'
    mock_deposit.return_value = conf_url
    response = await client.post('api/transactions/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    assert json_resp['confirmation_url'] == conf_url
