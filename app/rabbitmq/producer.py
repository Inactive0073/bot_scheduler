import asyncio
import aiormq

# from app.config_data.config import load_config


async def producer():
    # url = load_config().rabbitmq.URL
    # Подключение к RabbitMQ
    # connection: AbstractConnection = await aiormq.connect(url)
    connection = await aiormq.connect("amqp://rabbitmqlogin:rabbitmqpassword@localhost/")

    
    # Создание канала
    channel = await connection.channel()
    
    # Объявление точки обмена (создается, если не существует)
    await channel.exchange_declare("test_exchange", exchange_type="direct")
    
    # Отправка сообщения в exchange
    await channel.basic_publish(
        body="Привет из RabbitMQ!".encode("utf-8"),
        exchange="test_exchange",
        routing_key="test_routing_key"
    )
    
    # Закрытие соединения
    await connection.close()
    

asyncio.run(producer())