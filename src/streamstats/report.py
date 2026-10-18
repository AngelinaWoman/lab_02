import json
from pathlib import Path


def save_report(stats: dict, output_path: Path) -> None:
    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(stats, file, ensure_ascii=False, indent=2)