import logging
from redis.client import Redis
from redis.exceptions import RedisError

from .interface import HealthChecker


logger = logging.getLogger(__name__)


class RedisHealthChecker(HealthChecker):
    def __init__(self, redis_client: Redis):
        self.name = "redis"
        self.__redis_client = redis_client

    def check(self) -> bool:
        try:
            self.__redis_client.ping()

            return True
        except RedisError as e:
            logger.exception("%s health check failed", self.name, exc_info=e)

            return False
