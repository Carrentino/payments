from src.integrations.youkassa import YouKassaClient


async def get_youkassa_client() -> YouKassaClient:
    return YouKassaClient()
