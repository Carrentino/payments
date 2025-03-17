from datetime import datetime

from src.integrations.schemas.users import UpdateBalanceMessage
from src.integrations.users import UsersKafkaProducer
from src.repositories.user_balance import UserBalanceRepository
from src.services.schemas.user_balance import UpdateBalance
from src.utils import decrypt_data


class UserBalanceService:
    def __init__(
        self,
        user_balance_repository: UserBalanceRepository,
        users_kafka: UsersKafkaProducer,
    ) -> None:
        self.user_balance_repository = user_balance_repository
        self.users_kafka = users_kafka

    async def sync_balances(self) -> bool:
        balances = await self.user_balance_repository.get_list()
        balances_to_update = []
        balances_to_sync = []
        for balance in balances:
            if (balance.sync_time is not None and balance.sync_time < balance.updated_at) or balance.sync_time is None:
                balance.sync_time = datetime.now()
                balances_to_update.append(balance)
                balances_to_sync.append(UpdateBalance(user_id=balance.user_id, balance=decrypt_data(balance.balance)))
        await self.user_balance_repository.update_many(balances_to_update)
        await self.users_kafka.send_synced_balances(UpdateBalanceMessage(balances=balances_to_sync))
        return True
