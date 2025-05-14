from taskiq import TaskiqScheduler

from .broker import broker
from taskiq.schedule_sources import LabelScheduleSource

from app.config_data.config import load_config, Config

config: Config = load_config()

scheduler = TaskiqScheduler(broker=broker, sources=[LabelScheduleSource(broker)])
