from datetime import datetime, timedelta
import logging
from sqlalchemy import select, update, func, case, and_
from sqlalchemy.dialects.postgresql import insert as upsert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.bot.db.models import User, Customer, Bonus


logger = logging.getLogger(__name__)
