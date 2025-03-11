from uuid import UUID

from helpers.sqlalchemy.base_model import Base
from sqlalchemy.orm import Mapped


class UserPaymentInfo(Base):
    __tablename__ = "user_payment_info"
    user_id: Mapped[UUID]
    rebill_id: Mapped[str]
