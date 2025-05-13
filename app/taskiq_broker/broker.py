import logging
from taskiq_nats import PullBasedJetStreamBroker
from taskiq_redis import RedisAsyncResultBackend, RedisScheduleSource
from taskiq import TaskiqScheduler, TaskiqEvents, TaskiqState
from taskiq.schedule_sources import LabelScheduleSource

from app.config_data.config import load_config, Config

config: Config = load_config()

broker = PullBasedJetStreamBroker(servers=config.nats.servers, queue="taskiq_queue")
# redis_result = RedisAsyncResultBackend(config.redis.url)
redis_source = RedisScheduleSource(config.redis.url)
scheduler = TaskiqScheduler(broker=broker, sources=[config.redis.url, LabelScheduleSource(broker)])


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def startup(state: TaskiqState) -> None:
    logging.basicConfig(
        level=logging.DEBUG,
        format="[%(asctime)s] #%(levelname)-8s %(filename)s:"
        "%(lineno)d - %(name)s - %(message)s",
    )
    logger = logging.getLogger(__name__)
    logger.info("Starting scheduler...")

    state.logger = logger
    await redis_source.startup()


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def shutdown(state: TaskiqState) -> None:
    state.logger.info("Scheduler stopped")