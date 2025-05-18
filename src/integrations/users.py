from helpers.kafka.producer import KafkaProducer

from src.integrations.schemas.users import UpdateBalanceMessage
from src.settings import get_settings


class UsersClient(KafkaProducer):
    balance_topic = get_settings().kafka.topic_user_balance

    def __init__(self) -> None:
        super().__init__(str(get_settings().kafka.bootstrap_servers))

    async def send_balance(self, message: UpdateBalanceMessage) -> None:
        await self.send_model_message(self.balance_topic, message)
