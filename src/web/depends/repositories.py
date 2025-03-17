from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.transaction import TransactionRepository
from src.repositories.user_balance import UserBalanceRepository


async def get_transaction_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> TransactionRepository:
    return TransactionRepository(session)


async def get_user_balance_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> UserBalanceRepository:
    return UserBalanceRepository(session)
