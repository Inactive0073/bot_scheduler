from typing import Any, Optional, Self

import ormsgpack
from aiogram.filters.state import StateType
from aiogram.fsm.state import State
from aiogram.fsm.storage.base import (
    BaseStorage,
    DefaultKeyBuilder,
    KeyBuilder,
    StorageKey
)

from nats.aio.client import Client
from nats.js import JetStreamContext
from nats.js.api import KeyValueConfig
from nats.js.errors import NotFoundError
from nats.js.kv import KeyValue


class NatsStorage(BaseStorage):
    """
    Реализация хранилища состояний FSM для aiogram на базе NATS Key-Value.
    
    Хранит данные в двух отдельных бакетах:
    - Состояния пользователей (fsm_states_bucket)
    - Пользовательские данные (fsm_data_bucket)

    Args:
        nc (Client): Клиент NATS
        js (JetStreamContext): Контекст JetStream
        key_builder (KeyBuilder, optional): Генератор ключей для хранения
        fsm_states_bucket (str): Бакет для состояний (default: "fsm_states_aiogram")
        fsm_data_bucket (str): Бакет для данных (default: "fsm_data_aiogram")

    """

    def __init__(
        self,
        nc: Client,
        js: JetStreamContext,
        key_builder: Optional[KeyBuilder] = None,
        fsm_states_bucket: str = "fsm_states_aiogram",
        fsm_data_bucket: str = "fsm_data_aiogram",  
    ) -> None:
        super().__init__()
        
        self.nc = nc
        self.js = js
        self.fsm_states_bucket = fsm_states_bucket
        self.fsm_data_bucket = fsm_data_bucket
        self._key_builder = key_builder or DefaultKeyBuilder(
            with_bot_id=True, 
            with_destiny=True
        )

    async def create_storage(self) -> Self:
        """
        Инициализирует Key-Value хранилища. 
        Создает бакеты если они не существуют.
        
        Returns:
            Self: Экземпляр хранилища с проинициализированными бакетами
        """
        self.kv_states = await self._get_kv_states()
        self.kv_data = await self._get_kv_data()
        return self
    
    async def _get_kv_states(self) -> KeyValue:
        """Создает/получает бакет для хранения состояний"""
        return await self.js.create_key_value(
            config=KeyValueConfig(
                bucket=self.fsm_states_bucket,
                history=5,  # Сохраняет последние 5 версий
                storage="file"  # Тип хранилища (file/memory)
            )
        )
        
    async def _get_kv_data(self) -> KeyValue:
        """Создает/получает бакет для хранения пользовательских данных"""
        return await self.js.create_key_value(
            config=KeyValueConfig(
                bucket=self.fsm_data_bucket,
                history=5,
                storage="file"
            )
        )
        
    async def set_state(
        self, 
        key: StorageKey, 
        state: StateType = None
    ) -> None:
        """
        Сохраняет состояние пользователя
        
        Args:
            key (StorageKey): Ключ состояния
            state (StateType): Состояние для сохранения (None для сброса)
        """
        state = state.state if isinstance(state, State) else state
        await self.kv_states.put(
            self._key_builder.build(key), 
            ormsgpack.packb(state or None)
        )
        
    async def get_state(self, key: StorageKey) -> Optional[str]:
        """
        Получает текущее состояние пользователя
        
        Args:
            key (StorageKey): Ключ состояния
            
        Returns:
            Optional[str]: Состояние или None если не найдено
        """
        try:
            entry = await self.kv_states.get(self._key_builder.build(key))
            return ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return None
    
    async def set_data(self, key: StorageKey, data: dict[str, Any]) -> None:
        """
        Сохраняет пользовательские данные
        
        Args:
            key (StorageKey): Ключ данных
            data (dict): Словарь с данными
        """
        await self.kv_data.put(
            self._key_builder.build(key), 
            ormsgpack.packb(data)
        )
        
    async def get_data(self, key: StorageKey) -> dict[str, Any]:
        """
        Получает пользовательские данные
        
        Args:
            key (StorageKey): Ключ данных
            
        Returns:
            dict: Словарь с данными или пустой словарь если не найдено
        """
        try:
            entry = await self.kv_data.get(self._key_builder.build(key))
            return ormsgpack.unpackb(entry.value)
        except NotFoundError:
            return {}
        
    async def close(self) -> None:
        """Закрывает соединение с NATS"""
        await self.nc.close()

    async def __aenter__(self) -> Self:
        return await self.create_storage()

    async def __aexit__(self, *args) -> None:
        await self.close()

# Примечания:
# 1. Требует предварительно настроенного NATS сервера с JetStream
# 2. Для production использовать persistence storage:
#    docker run -p 4222:4222 -v /nats-data:/data nats -js --store_dir /data
# 3. KeyBuilder по умолчанию включает bot_id и destiny для предотвращения коллизий
# 4. ormsgpack обеспечивает высокопроизводительную сериализацию