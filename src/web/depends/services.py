from typing import Annotated

from fastapi import Depends

from src.integrations.youkassa import YouKassaClient
from src.repositories.transaction import TransactionRepository
from src.services.transaction import TransactionService
from src.web.depends.integrations import get_youkassa_client
from src.web.depends.repositories import get_transaction_repository


async def get_transaction_service(
    transaction_repository: Annotated[TransactionRepository, Depends(get_transaction_repository)],
    youkassa_client: Annotated[YouKassaClient, Depends(get_youkassa_client)],
) -> TransactionService:
    return TransactionService(
        transaction_repository=transaction_repository,
        youkassa_client=youkassa_client,
    )
