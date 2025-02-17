from dataclasses import dataclass
from environs import Env


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class RabbitMQConfig:
    URL: str


@dataclass
class Config:
    tg_bot: TgBot
    rabbitmq: RabbitMQConfig


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)

    rabbitmq_url = f"amqp://{env('RABBITMQ_USER')}:"
    f"{env('RABBITMQ_PASS')}@"
    f"{env('RABBITMQ_IP')}:env{'RABBITMQ_PORT'}"

    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")), rabbitmq=RabbitMQConfig(HOST=rabbitmq_url)
    )
