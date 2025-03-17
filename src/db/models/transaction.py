from decimal import Decimal
from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from src.db.enums.transaction import TransactionStatus, TransactionType


class Transaction(Base):
    __tablename__ = 'transactions'
    user_id: Mapped[UUID]
    amount: Mapped[Decimal]
    transaction_type: Mapped[TransactionType] = mapped_column(Enum(TransactionType))
    status: Mapped[TransactionStatus] = mapped_column(Enum(TransactionStatus), default=TransactionStatus.PENDING)
    payment_redirect: Mapped[str]
    confirmation_url: Mapped[str] = mapped_column(nullable=True)
