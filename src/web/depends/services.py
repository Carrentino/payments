from typing import Annotated

from fastapi import Depends

from src.integrations.users import UsersClient
from src.integrations.youkassa import YouKassaClient
from src.repositories.transaction import TransactionRepository
from src.repositories.user_balance import UserBalanceRepository
from src.services.transaction import TransactionService
from src.services.user_balance import UserBalanceService
from src.web.depends.integrations import get_users_clint
from src.web.depends.integrations import get_youkassa_client
from src.web.depends.repositories import get_transaction_repository, get_user_balance_repository


async def get_transaction_service(
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
    user_balance_repository: Annotated[UserBalanceRepository, Depends(get_user_balance_repository)],
    youkassa_client: Annotated[YouKassaClient, Depends(get_youkassa_client)],
    users_client: Annotated[UsersClient, Depends(get_users_clint)],
) -> TransactionService:
    return TransactionService(
        transaction_repository=transaction_repository,
        user_balance_repository=user_balance_repository,
        youkassa_client=youkassa_client,
        users_client=users_client,
    )


async def get_user_balance_service(
    user_balance_repository: Annotated[UserBalanceRepository, Depends(get_user_balance_repository)],
    users_client: Annotated[UsersClient, Depends(get_users_clint)],
) -> UserBalanceService:
    return UserBalanceService(
        user_balance_repository=user_balance_repository,
        users_client=users_client,
    )
