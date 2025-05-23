import logging
import asyncio
from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import delete, text
from sqlalchemy.exc import SQLAlchemyError

from app.bot.db.base import Base
from app.config_data.config import Config, load_config
from app.bot.db.models.bonuses import Bonus
from app.taskiq_broker.broker import broker

logger = logging.getLogger(__name__)


@broker.task(task_name="delete_old_or_empty_bonus", schedule=[{"cron": "* * * * *"}])
async def delete_empty_bonus():
    config: Config = load_config()
    
    engine = create_async_engine(url=config.db.dsn, echo=config.db.is_echo)
    async with engine.begin() as conn:
        try:
            print(f"CONN OBJECTS IS WAS ACCEPTED {conn}")
            current_time = datetime.now(timezone.utc)
            stmt = delete(Bonus).where(Bonus.amount == 0, Bonus.expire_date < current_time)
        
            result = await conn.execute(stmt)
            logger.info(f"Удалено {result.rowcount} записей из таблицы бонусов.")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении записей бонусов: {e}")