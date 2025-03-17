from uuid import uuid4

import factory

from src.db.enums.transaction import TransactionType, TransactionStatus
from src.db.models.transaction import Transaction
from tests.factories.base import BaseSqlAlchemyFactory


class TransactionFactory(BaseSqlAlchemyFactory):
    class Meta:
        model = Transaction

    user_id = factory.LazyAttribute(lambda _: uuid4())
    amount = factory.Faker('pydecimal', left_digits=1, right_digits=1, positive=True)
    transaction_type = factory.Iterator(TransactionType)
    status = factory.Iterator(TransactionStatus)
    payment_redirect = factory.Faker('word')
