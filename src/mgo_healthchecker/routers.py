from typing import Annotated, Callable

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from .utils import HealthCheckerCollection


def create_router(
    get_health_checker_collection: Callable[[], HealthCheckerCollection],
) -> APIRouter:
    router = APIRouter()

    @router.get(
        "/health",
    )
    def health(
        health_checkers: Annotated[
            HealthCheckerCollection, Depends(get_health_checker_collection)
        ],
    ) -> JSONResponse:
        components = [health_checker.to_dict() for health_checker in health_checkers]
        is_healthy: bool = all(component["is_healthy"] for component in components)

        return JSONResponse(
            content={"is_healthy": is_healthy, "components": components},
            status_code=200 if is_healthy else 503,
        )

    return router
