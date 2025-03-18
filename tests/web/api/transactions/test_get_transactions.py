from uuid import uuid4

from httpx import AsyncClient
from starlette import status

from src.db.enums.transaction import TransactionType
from tests.factories.transaction import TransactionFactory


async def test_get_transactions(client: AsyncClient) -> None:
    user_id = uuid4()
    await TransactionFactory.create(user_id=user_id, transaction_type=TransactionType.DEPOSIT)
    await TransactionFactory.create(user_id=user_id, transaction_type=TransactionType.DEPOSIT)
    await TransactionFactory.create(user_id=user_id, transaction_type=TransactionType.WITHDRAW)

    response = await client.get(f"/api/transactions/{user_id}/?transaction_type={TransactionType.DEPOSIT}")
    assert response.status_code == status.HTTP_200_OK
    json_resp = response.json()
    assert json_resp["total"] == 2
