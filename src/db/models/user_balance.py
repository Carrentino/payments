from datetime import datetime
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped, mapped_column


class UserBalance(Base):
    __tablename__ = "user_balances"
    user_id: Mapped[UUID]
    balance: Mapped[str]
    sync_time: Mapped[datetime] = mapped_column(nullable=True)
