from fastapi import FastAPI
from fastapi.testclient import TestClient

from mgo_healthchecker.services.interface import HealthChecker
from mgo_healthchecker.routers import create_router
from mgo_healthchecker.utils import HealthCheckerCollection


class HealthyTestHealthChecker(HealthChecker):
    name = "healthy_test"

    def check(self) -> bool:
        return True


class UnhealthyTestHealthChecker(HealthChecker):
    name = "unhealthy_test"

    def check(self) -> bool:
        return False


class TestPackage:
    def test_it_returns_a_healthy_status(self) -> None:
        def get_collection() -> HealthCheckerCollection:
            collection = HealthCheckerCollection()

            collection.append(HealthyTestHealthChecker())

            return collection

        app = FastAPI()
        app.include_router(create_router(get_collection))
        client = TestClient(app)

        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {
            "is_healthy": True,
            "components": [
                {
                    "name": "healthy_test",
                    "is_healthy": True,
                }
            ],
        }

    def test_it_returns_an_unhealthy_status(self) -> None:
        def get_collection() -> HealthCheckerCollection:
            collection = HealthCheckerCollection()

            collection.append(HealthyTestHealthChecker())
            collection.append(UnhealthyTestHealthChecker())

            return collection

        app = FastAPI()
        app.include_router(create_router(get_collection))
        client = TestClient(app)

        response = client.get("/health")

        assert response.status_code == 503
        assert response.json() == {
            "is_healthy": False,
            "components": [
                {
                    "name": "healthy_test",
                    "is_healthy": True,
                },
                {
                    "name": "unhealthy_test",
                    "is_healthy": False,
                },
            ],
        }
