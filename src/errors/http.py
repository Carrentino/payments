from helpers.errors import ServerError
from starlette import status


class InsufficientFundsHttpError(ServerError):
    message = "Insufficient funds"
    status_code = status.HTTP_409_CONFLICT


class TransactionNotFoundHttpError(ServerError):
    message = "Transaction not found"
    status_code = status.HTTP_404_NOT_FOUND
