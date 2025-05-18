from helpers.errors import BaseError


class InsufficientFundsError(BaseError):
    message = "Insufficient funds"


class TransactionNotFoundError(BaseError):
    message = "Transaction not found"
