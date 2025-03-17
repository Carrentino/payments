from uuid import uuid4

import factory

from src.db.models.user_balance import UserBalance
from src.utils import encrypt_data
from tests.factories.base import BaseSqlAlchemyFactory


class UserBalanceFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = UserBalance

    balance = factory.LazyAttribute(lambda _: encrypt_data('3000.00'))
    user_id = factory.LazyAttribute(lambda _: uuid4())
