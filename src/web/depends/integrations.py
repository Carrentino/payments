from src.integrations.users import UsersClient
from src.integrations.youkassa import YouKassaClient


async def get_youkassa_client() -> YouKassaClient:
    return YouKassaClient()


async def get_users_clint() -> UsersClient:
    return UsersClient()
