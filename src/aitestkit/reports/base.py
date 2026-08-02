from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseReportGenerator(ABC):
    """Abstract Base Class for all Report Exporters."""

    @classmethod
    @abstractmethod
    def generate(cls, data: Dict[str, Any], output_path: str) -> str:
        """Abstract method to export test data into specific report file format."""
        pass