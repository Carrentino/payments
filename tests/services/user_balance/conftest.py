import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.user_balance import UserBalanceService
from src.web.depends.integrations import get_users_kafka
from src.web.depends.repositories import get_user_balance_repository


@pytest.fixture()
async def user_balance_service(session: AsyncSession) -> UserBalanceService:
    return UserBalanceService(
        user_balance_repository=await get_user_balance_repository(session=session),
        users_kafka=await get_users_kafka(),
    )
