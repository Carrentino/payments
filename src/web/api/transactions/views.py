from typing import Annotated

from fastapi import APIRouter, Depends

from src.errors.http import InsufficientFundsHttpError
from src.errors.service import InsufficientFundsError
from src.services.transaction import TransactionService
from src.web.api.transactions.schemas import DepositOrWithdrawReq, DepositOrWithdrawResp
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
