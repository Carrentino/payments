from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped


class UserBalance(Base):
    __tablename__ = "user_balances"
    user_id: Mapped[UUID]
    balance: Mapped[str]
