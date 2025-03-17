from src.integrations.users import UsersKafkaProducer
from src.integrations.youkassa import YouKassaClient


async def get_youkassa_client() -> YouKassaClient:
    return YouKassaClient()


async def get_users_kafka() -> UsersKafkaProducer:
    return UsersKafkaProducer()
