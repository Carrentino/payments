from typing import Any

from helpers.sqlalchemy.base_repo import ISqlAlchemyRepository
from sqlalchemy import select, func

from src.db.models.transaction import Transaction


class TransactionRepository(ISqlAlchemyRepository[Transaction]):
    _model = Transaction

    async def get_paginated_transactions(
        self, limit: int = 30, offset: int = 0, **filters: Any
    ) -> tuple[list[Transaction], Any | None]:
        query = select(self._model)

        if filters:
            query = query.filter_by(**filters)

        count_query = select(func.count()).select_from(query.subquery().alias("subq"))
        objects_query = query.limit(limit).offset(offset)

        result = list(await self.session.scalars(objects_query))
        count_result = await self.session.execute(count_query)
        total = count_result.scalar()
        return result, total
