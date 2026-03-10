from typing import List

from .services.interface import HealthChecker


class HealthCheckerCollection(List[HealthChecker]):
    pass
