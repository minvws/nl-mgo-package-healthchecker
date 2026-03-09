from typing import List

from .services import HealthChecker


class HealthCheckerCollection(List[HealthChecker]):
    pass
