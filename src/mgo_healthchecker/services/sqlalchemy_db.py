import logging
from sqlalchemy import text
from sqlalchemy.engine import Engine

from .interface import HealthChecker


logger = logging.getLogger(__name__)


class SqlAlchemyDbHealthChecker(HealthChecker):
    def __init__(self, db_engine: Engine):
        self.name = "db"
        self.__db_engine = db_engine

    def check(self) -> bool:
        try:
            with self.__db_engine.connect() as conn:
                conn.scalar(text("SELECT 1"))

            return True
        except Exception as e:
            logger.exception("%s health check failed", self.name, exc_info=e)

            return False
