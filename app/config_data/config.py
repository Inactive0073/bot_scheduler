from dataclasses import dataclass
from environs import Env

from typing import List


@dataclass
class TgBot:
    token: str  # Токен для доступа к телеграм-боту


@dataclass
class NatsConfig:
    servers: List[str]


@dataclass
class NatsDelayedConsumerConfig:
    subject_channel: str
    subject_subscriber: str
    stream: str
    durable_name: str


@dataclass
class DataBase:
    dsn: str
    is_echo: bool


@dataclass
class Config:
    tg_bot: TgBot
    nats: NatsConfig
    delayed_consumer: NatsDelayedConsumerConfig
    db: DataBase


def load_config(path: str | None = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(token=env("BOT_TOKEN")),
        nats=NatsConfig(servers=env.list("NATS_SERVERS")),
        delayed_consumer=NatsDelayedConsumerConfig(
            subject_channel=env("NATS_DELAYED_CONSUMER_SUBJECT_CHANNEL"),
            subject_subscriber=env("NATS_DELAYED_CONSUMER_SUBJECT_SUBSCRIBER"),
            stream=env("NATS_DELAYED_CONSUMER_STREAM"),
            durable_name=env("NATS_DELAYED_CONSUMER_DURABLE_NAME"),
        ),
        db=DataBase(dsn=env("DSN"), is_echo=env.bool(("IS_ECHO"))),
    )
