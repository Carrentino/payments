from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from helpers.utils import get_paginated_response

from src.errors.http import InsufficientFundsHttpError
from src.errors.service import InsufficientFundsError
from src.services.transaction import TransactionService
from src.web.api.transactions.schemas import DepositOrWithdrawReq, DepositOrWithdrawResp, TransactionFilters
from src.web.depends.services import get_transaction_service

transactions_router = APIRouter()


@transactions_router.post('/')
async def deposit_or_withdraw(
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)], req_data: DepositOrWithdrawReq
) -> DepositOrWithdrawResp:
    try:
        return await transaction_service.process_transaction(req_data)
    except InsufficientFundsError:
        raise InsufficientFundsHttpError from None


@transactions_router.get('/{user_id}/')
async def get_transactions(
    transaction_service: Annotated[TransactionService, Depends(get_transaction_service)],
    user_id: UUID,
    filters: TransactionFilters = Depends(),
):
    data, count = await transaction_service.get_transactions(user_id, filters)
    return await get_paginated_response(data=data, count=count, limit=filters.limit, offset=filters.offset)
