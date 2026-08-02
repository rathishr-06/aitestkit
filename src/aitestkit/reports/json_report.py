import json
from pathlib import Path
from typing import Dict, Any
from aitestkit.reports.base import BaseReportGenerator


class JSONReportGenerator(BaseReportGenerator):
    """Generates JSON Benchmark Summary Reports."""

    @classmethod
    def generate(cls, data: Dict[str, Any], output_path: str = "reports/summary.json") -> str:
        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        return str(path)