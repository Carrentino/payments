from typing import Annotated

from fastapi import Depends

from src.integrations.users import UsersKafkaProducer
from src.integrations.youkassa import YouKassaClient
from src.repositories.transaction import TransactionRepository
from src.repositories.user_balance import UserBalanceRepository
from src.services.transaction import TransactionService
from src.services.user_balance import UserBalanceService
from src.web.depends.integrations import get_youkassa_client, get_users_kafka
from src.web.depends.repositories import get_transaction_repository, get_user_balance_repository


async def get_transaction_service(
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
    user_balance_repository: Annotated[UserBalanceRepository, Depends(get_user_balance_repository)],
    youkassa_client: Annotated[YouKassaClient, Depends(get_youkassa_client)],
) -> TransactionService:
    return TransactionService(
        transaction_repository=transaction_repository,
        user_balance_repository=user_balance_repository,
        youkassa_client=youkassa_client,
    )


async def get_user_balance_service(
    user_balance_repository: Annotated[UserBalanceRepository, Depends(get_user_balance_repository)],
    users_kafka: Annotated[UsersKafkaProducer, Depends(get_users_kafka)],
) -> UserBalanceService:
    return UserBalanceService(
        user_balance_repository=user_balance_repository,
        users_kafka=users_kafka,
    )
