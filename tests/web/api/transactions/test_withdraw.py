from decimal import Decimal
from unittest.mock import patch, AsyncMock
from uuid import uuid4

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.db.enums.transaction import TransactionType
from src.utils import decrypt_data
from src.web.api.transactions.schemas import DepositOrWithdrawReq
from tests.factories.user_balance import UserBalanceFactory


@patch('src.integrations.youkassa.YouKassaClient.withdraw', new_callable=AsyncMock)
async def test_withdraw_ok(
    mock_deposit: AsyncMock, client: AsyncClient, session: AsyncSession  # noqa: ARG001
) -> None:  # noqa: ARG001
    user_balance = await UserBalanceFactory.create()
    req = DepositOrWithdrawReq(
        user_id=user_balance.user_id,
        amount=Decimal(100.00),
        transaction_type=TransactionType.WITHDRAW,
        card_number='string',
    )
    response = await client.post('api/transactions/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_200_OK
    await session.refresh(user_balance)
    assert decrypt_data(user_balance.balance) == '2900.00'


@patch('src.integrations.youkassa.YouKassaClient.withdraw', new_callable=AsyncMock)
async def test_withdraw_not_balance(
    mock_deposit: AsyncMock, client: AsyncClient  # noqa: ARG001
) -> None:  # noqa: ARG001
    req = DepositOrWithdrawReq(
        user_id=uuid4(), amount=Decimal(10.10), transaction_type=TransactionType.WITHDRAW, card_number='string'
    )
    response = await client.post('api/transactions/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_409_CONFLICT


@patch('src.integrations.youkassa.YouKassaClient.withdraw', new_callable=AsyncMock)
async def test_withdraw_not_money(
    mock_deposit: AsyncMock, client: AsyncClient, session: AsyncSession  # noqa: ARG001
) -> None:  # noqa: ARG001
    user_balance = await UserBalanceFactory.create()
    req = DepositOrWithdrawReq(
        user_id=user_balance.user_id,
        amount=Decimal(5000.10),
        transaction_type=TransactionType.WITHDRAW,
        card_number='string',
    )
    response = await client.post('api/transactions/', json=req.model_dump(mode='json'))
    assert response.status_code == status.HTTP_409_CONFLICT
    await session.refresh(user_balance)
    assert decrypt_data(user_balance.balance) == '3000.00'
