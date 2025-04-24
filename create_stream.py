import asyncio

import nats
from nats.aio.client import Client
from nats.js.api import StreamConfig
from nats.js.client import JetStreamContext
from nats.js.api import RetentionPolicy, StorageType

from app.config_data.config import Config, load_config


async def main():
    config: Config = load_config()
    # Подключаемся к NATS серверу
    nc: Client = await nats.connect("nats://127.0.0.1:4222")
    # Получаем JetStream-контекст
    js: JetStreamContext = nc.jetstream()

    # Настройка стрима с заданными параметрами
    stream_config = StreamConfig(
        name=config.delayed_consumer.stream,  # Название стрима
        # Список сабжектов
        subjects=[
            config.delayed_consumer.subject_channel,
            config.delayed_consumer.subject_subscriber,
        ],
        retention=RetentionPolicy.LIMITS,  # Политика удержания
        max_bytes=3000 * 1024 * 1024,  # 3000 MiB
        max_msg_size=10 * 1024 * 1024,  # 10 MiB
        storage=StorageType.FILE,  # Хранение сообщений на диске
        allow_direct=True,  # Разрешение получать сообщения без создания консьюмера
    )

    await js.add_stream(config=stream_config)

    print("Stream `SocialMediaStream` created successfully.")


if __name__ == "__main__":
    asyncio.run(main())
