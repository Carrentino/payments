from pydantic import BaseModel

from src.services.schemas.user_balance import UpdateBalance


class UpdateBalanceMessage(BaseModel):
    balances: list[UpdateBalance]
