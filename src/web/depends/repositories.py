from typing import Annotated

from fastapi import Depends
from helpers.depends.db_session import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.transaction import TransactionRepository


async def get_transaction_repository(
    session: Annotated[AsyncSession, Depends(get_db_session)]
) -> TransactionRepository:
    return TransactionRepository(session)
