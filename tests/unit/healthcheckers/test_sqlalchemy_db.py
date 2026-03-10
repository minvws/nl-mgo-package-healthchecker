from pytest_mock import MockerFixture

from sqlalchemy import Connection
from sqlalchemy.engine import Engine

from mgo_healthchecker.services.sqlalchemy_db import SqlAlchemyDbHealthChecker


class TestSqlAlchemyDbHealthChecker:
    def test_name_is_set(self, mocker: MockerFixture) -> None:
        mock_db_engine = mocker.Mock(spec=Engine)

        sut = SqlAlchemyDbHealthChecker(db_engine=mock_db_engine)

        assert sut.name == "db"

    def test_check_returns_true_if_select_succeeds(self, mocker: MockerFixture) -> None:
        mock_db_engine = mocker.Mock(spec=Engine)
        mock_conn = mocker.Mock(spec=Connection)

        mock_db_engine.connect = mocker.MagicMock()
        mock_db_engine.connect.return_value.__enter__.return_value = mock_conn

        sut = SqlAlchemyDbHealthChecker(db_engine=mock_db_engine)

        assert sut.check() is True

        mock_db_engine.connect.assert_called_once()
        mock_conn.scalar.assert_called_once()

    def test_check_returns_false_on_failure(self, mocker: MockerFixture) -> None:
        mock_db_engine = mocker.Mock(spec=Engine)
        mock_logger = mocker.patch("mgo_healthchecker.services.sqlalchemy_db.logger")
        exception = Exception("Connection failed")

        mock_db_engine.connect = mocker.MagicMock()
        mock_db_engine.connect.side_effect = exception

        sut = SqlAlchemyDbHealthChecker(db_engine=mock_db_engine)

        assert sut.check() is False

        mock_db_engine.connect.assert_called_once()
        mock_logger.exception.assert_called_once_with(
            "%s health check failed",
            sut.name,
            exc_info=exception,
        )
