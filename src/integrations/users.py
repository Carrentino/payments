from helpers.kafka.producer import KafkaProducer

from src.integrations.schemas.users import UpdateBalanceMessage
from src.settings import get_settings


class UsersKafkaProducer(KafkaProducer):
    email_topic = get_settings().kafka.topic_user_payment

    def __init__(self) -> None:
        super().__init__(str(get_settings().kafka.users_url))

    async def send_synced_balances(self, message: UpdateBalanceMessage) -> None:
        await self.send_model_message(self.email_topic, message)
