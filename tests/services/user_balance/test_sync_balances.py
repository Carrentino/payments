from unittest.mock import patch, AsyncMock

from src.services.user_balance import UserBalanceService
from tests.factories.user_balance import UserBalanceFactory


@patch('src.integrations.users.UsersKafkaProducer.send_synced_balances', new_callable=AsyncMock)
async def test_sync_balances(mock_send: AsyncMock, user_balance_service: UserBalanceService):  # noqa: ARG001
    await UserBalanceFactory.create()
    res = await user_balance_service.sync_balances()
    assert res
