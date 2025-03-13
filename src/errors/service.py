from helpers.errors import BaseError


class InsufficientFundsError(BaseError):
    message = "Insufficient funds"
