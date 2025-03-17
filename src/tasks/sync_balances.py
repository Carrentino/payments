import asyncio

from celery import shared_task
from helpers.depends.db_session import get_db_session_context

from src.tasks.db_client import make_db_client
from src.web.depends.repositories import get_user_balance_repository
from src.web.depends.services import get_user_balance_service


@shared_task(name="sync_balances_task")  # type: ignore
def sync_balances_task():
    asyncio.run(run_async_task())


async def run_async_task() -> None:
    async with get_db_session_context(make_db_client()) as session:
        service = get_user_balance_service(user_balance_repository=await get_user_balance_repository(session=session))
        await service.sync_balances()
