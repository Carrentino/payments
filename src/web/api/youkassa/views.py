from typing import Annotated

from fastapi import APIRouter, Depends

from src.errors.http import TransactionNotFoundHttpError
from src.errors.service import TransactionNotFoundError
from src.services.transaction import TransactionService
from src.web.depends.services import get_transaction_service

youkassa_router = APIRouter()


@youkassa_router.get("/")
async def webhook(transaction_service: Annotated[TransactionService, Depends(get_transaction_service)], data: dict):
    try:
        await transaction_service.process_webhook(data)
    except TransactionNotFoundError:
        raise TransactionNotFoundHttpError from None
