from abc import ABC, abstractmethod
import logging
from typing import Dict

from redis.client import Redis
from redis.exceptions import RedisError
from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)


class HealthChecker(ABC):
    name: str

    @abstractmethod
    def check(self) -> bool: ...

    def to_dict(self) -> Dict[str, str | bool]:
        return {
            "name": self.name,
            "is_healthy": self.check(),
        }


class PostgreSQLHealthChecker(HealthChecker):
    def __init__(self, db_engine: Engine):
        self.name = "postgresql"
        self.__db_engine = db_engine

    def check(self) -> bool:
        try:
            with self.__db_engine.connect() as conn:
                conn.scalar(text("SELECT 1"))

            return True
        except Exception as e:
            logger.exception("%s health check failed", self.name, exc_info=e)

            return False


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
