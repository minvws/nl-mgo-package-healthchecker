from pytest_mock import MockerFixture

from redis import Redis, RedisError

from mgo_healthchecker.redis import RedisHealthChecker


class TestRedisHealthChecker:
    def test_init_sets_name(self, mocker: MockerFixture) -> None:
        mock_redis_client = mocker.Mock(spec=Redis)

        sut = RedisHealthChecker(redis_client=mock_redis_client)

        assert sut.name == "redis"

    def test_check_when_ping_succeeds_returns_true(self, mocker: MockerFixture) -> None:
        mock_redis_client = mocker.Mock(spec=Redis)

        mock_redis_client.ping.return_value = True

        sut = RedisHealthChecker(redis_client=mock_redis_client)

        assert sut.check() is True

        mock_redis_client.ping.assert_called_once()

    def test_check_when_ping_fails_returns_false(self, mocker: MockerFixture) -> None:
        mock_redis_client = mocker.Mock(spec=Redis)
        mock_logger = mocker.patch("mgo_healthchecker.redis.logger")
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
