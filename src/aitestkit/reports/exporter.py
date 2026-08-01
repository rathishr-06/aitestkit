from dataclasses import asdict
import json
from pathlib import Path


class ReportExporter:

    @staticmethod
    def export_json(data: dict | list, filepath: str) -> None:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def export_csv(
        data: list[dict], filepath: str, headers: list[str] | None = None
    ) -> None:
        import csv

        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)

        if not data:
            return

        keys = headers if headers else list(data[0].keys())

        with open(path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(data)