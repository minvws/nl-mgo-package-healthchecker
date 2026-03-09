from pytest_mock import MockerFixture

from redis import Redis, RedisError
from sqlalchemy import Connection
from sqlalchemy.engine import Engine

from mgo_healthchecker.services import PostgreSQLHealthChecker, RedisHealthChecker


class TestPostgreSQLHealthChecker:
    def test_name_is_set(self, mocker: MockerFixture) -> None:
        mock_db_engine = mocker.Mock(spec=Engine)

        sut = PostgreSQLHealthChecker(db_engine=mock_db_engine)

        assert sut.name == "postgresql"

    def test_check_returns_true_if_select_succeeds(self, mocker: MockerFixture) -> None:
        mock_db_engine = mocker.Mock(spec=Engine)
        mock_conn = mocker.Mock(spec=Connection)

        mock_db_engine.connect = mocker.MagicMock()
        mock_db_engine.connect.return_value.__enter__.return_value = mock_conn

        sut = PostgreSQLHealthChecker(db_engine=mock_db_engine)

        assert sut.check() is True

        mock_db_engine.connect.assert_called_once()
        mock_conn.scalar.assert_called_once()

    def test_check_returns_false_on_failure(self, mocker: MockerFixture) -> None:
        mock_db_engine = mocker.Mock(spec=Engine)
        mock_logger = mocker.patch("mgo_healthchecker.services.logger")
        exception = Exception("Connection failed")

        mock_db_engine.connect = mocker.MagicMock()
        mock_db_engine.connect.side_effect = exception

        sut = PostgreSQLHealthChecker(db_engine=mock_db_engine)

        assert sut.check() is False

        mock_db_engine.connect.assert_called_once()
        mock_logger.exception.assert_called_once_with(
            "%s health check failed",
            sut.name,
            exc_info=exception,
        )


class TestRedisHealthChecker:
    def test_name_is_set(self, mocker: MockerFixture) -> None:
        mock_redis_client = mocker.Mock(spec=Redis)

        sut = RedisHealthChecker(redis_client=mock_redis_client)

        assert sut.name == "redis"

    def test_check_returns_true_if_ping_succeeds(self, mocker: MockerFixture) -> None:
        mock_redis_client = mocker.Mock(spec=Redis)

        mock_redis_client.ping.return_value = True

        sut = RedisHealthChecker(redis_client=mock_redis_client)

        assert sut.check() is True

        mock_redis_client.ping.assert_called_once()

    def test_check_returns_false_on_failure(self, mocker: MockerFixture) -> None:
        mock_redis_client = mocker.Mock(spec=Redis)
        mock_logger = mocker.patch("mgo_healthchecker.services.logger")
        exception = RedisError("Redis error")

        mock_redis_client.ping.side_effect = exception

        sut = RedisHealthChecker(redis_client=mock_redis_client)

        assert sut.check() is False

        mock_redis_client.ping.assert_called_once()
        mock_logger.exception.assert_called_once_with(
            "%s health check failed",
            sut.name,
            exc_info=exception,
        )
