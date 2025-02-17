import asyncio

import aiormq
from aiormq.abc import DeliveredMessage

# from app.config_data.config import load_config

# callback, вызываемый на каждое сообщение для консьюмера
async def on_message(message: DeliveredMessage):
    print(message.body.decode())
    
    # Явное подтверждение получения и обработки ошибки
    await message.channel.basic_ack(delivery_tag=message.delivery.delivery_tag)
    

async def main():
    # Подключение к RabbitMQ
    # url = load_config().rabbitmq.URL
    # connection = await aiormq.connect(url)
    connection = await aiormq.connect("amqp://rabbitmqlogin:rabbitmqpassword@localhost/")
    
    
    # Создание канала
    channel = await connection.channel()
    
    # Объявление точки обмена 
    await channel.exchange_declare("test_exchange", exchange_type="direct")
    
    # Объявление очереди (создается, если не существует)
    declare_ok = await channel.queue_declare("test_done")
    
    # Привязка очереди к точке обмена
    await channel.queue_bind(
        queue=declare_ok.queue,
        exchange="test_exchange",
        routing_key="test_routing_key"
    )
    
    # Определение количества сообщений, которые консьюмер может получить за один раз
    await channel.basic_qos(prefetch_count=1)
    
    # Настройка прослушивания очереди
    await channel.basic_consume(declare_ok.queue, on_message)
    
    await asyncio.Future()
    
asyncio.run(main())