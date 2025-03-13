from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository

from src.db.models.user_balance import UserBalance


class UserBalanceRepository(ISqlAlchemyRepository[UserBalance]):
    _model = UserBalance
