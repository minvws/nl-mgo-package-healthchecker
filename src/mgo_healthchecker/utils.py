from typing import List

from .interface import HealthChecker


class HealthCheckerCollection(List[HealthChecker]):
    pass
