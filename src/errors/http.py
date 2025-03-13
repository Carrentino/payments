from helpers.errors import ServerError
from starlette import status


class InsufficientFundsHttpError(ServerError):
    message = "Insufficient funds"
    status_code = status.HTTP_409_CONFLICT
