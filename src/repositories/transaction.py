from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.transaction import Transaction


class TransactionRepository(ISqlAlchemyRepository[Transaction]):
    _model = Transaction
