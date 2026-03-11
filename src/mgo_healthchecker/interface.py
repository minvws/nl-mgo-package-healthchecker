from abc import ABC, abstractmethod

from typing import Dict


class HealthChecker(ABC):
    name: str

    @abstractmethod
    def check(self) -> bool: ...

    def to_dict(self) -> Dict[str, str | bool]:
        return {
            "name": self.name,
            "is_healthy": self.check(),
        }
