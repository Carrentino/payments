from functools import lru_cache

from pydantic import Field, PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class YouKassaSettings(BaseSettings):
    api_key: SecretStr
    account_id: SecretStr
    url: str
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix="youkassa_",
    )


class KafkaSettings(BaseSettings):
    users_url: str
    bootstrap_servers: str = Field(default='localhost:9092')
    group_id: str = Field(default='payments-group')
    topic_user_balance: str = Field(default='users_balance')

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix="kafka_",
    )


class RedisSettings(BaseSettings):
    url: str
    celery_db: int
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
        env_prefix="redis_",
    )


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        str_strip_whitespace=True,
        validate_default=True,
        case_sensitive=False,
        extra='ignore',
    )

    host: str = '127.0.0.1'
    port: int = 8080
    workers_count: int = 1
    reload: bool = True

    log_level: str = Field(default='info')
    debug: bool = True
    debug_postgres: bool = False

    environment: str = 'dev'

    postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:postgres@localhost:5432/base'
    )
    test_postgres_dsn: PostgresDsn = Field(  # type: ignore
        default='postgresql+asyncpg://postgres:@localhost:5432/base_test'
    )
    youkassa: YouKassaSettings = YouKassaSettings()
    kafka: KafkaSettings = KafkaSettings()

    trace_id_header: str = 'X-Trace-Id'
    jwt_key: SecretStr = Field(default=SecretStr('551b8ef09b5e43ddcc45461f854a89b83b9277c6e578f750bf5a6bc3f06d8c08'))
    payment_redirect: str = Field(default='http://localhost:8080')
    crypto_key: bytes = Field(
        default=b'\x17]~X#\r\xbb\xf3X\x88\x92}\x9aj\xa4\xcd\xe3\xdfZ\xe7\xdaF\xca\xbe\xfb\x9d\x9c\x08\x9eY2\xa6'
    )
    redis: RedisSettings = RedisSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()
