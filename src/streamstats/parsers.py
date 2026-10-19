import csv
import json
import logging
from collections.abc import Iterator
from pathlib import Path

from streamstats.errors import (
    InvalidEventError,
    StreamStatsError,
    UnsupportedFormatError,
)
from streamstats.models import validate_event

logger = logging.getLogger(__name__)


def parse_jsonl(
    path: Path, skipped: dict, skip_invalid: bool = False
) -> Iterator[dict[str, str]]:
    with open(path, encoding="utf-8") as file:
        line_number = 0
        for line in file:
            line_number += 1
            try:
                event = json.loads(line)
                validate_event(event)
            except json.JSONDecodeError as error:
                if skip_invalid:
                    logger.warning(
                        "Пропущена некорректная строка %s в файле %s: %s",
                        line_number,
                        path,
                        error,
                    )
                    skipped["count"] += 1
                    continue
                raise InvalidEventError(
                    f"Ошибка: {error}, в файле: {path}, в строке: {line_number}"
                )
            except StreamStatsError as error:
                if skip_invalid:
                    logger.warning(
                        "Пропущена некорректная строка %s в файле %s: %s",
                        line_number,
                        path,
                        error,
                    )
                    skipped["count"] += 1
                    continue
                raise StreamStatsError(
                    f"Ошибка: {error}, в файле: {path}, в строке: {line_number}"
                ) from error
            yield event


def parse_csv(
    path: Path, skipped: dict, skip_invalid: bool = False
) -> Iterator[dict[str, str]]:
    with open(path, encoding="utf-8") as file:
        line_number = 1
        dict_csv = csv.DictReader(file)
        for event in dict_csv:
            line_number += 1
            try:
                validate_event(event)
            except StreamStatsError as error:
                if skip_invalid:
                    logger.warning(
                        "Пропущена некорректная строка %s в файле %s: %s",
                        line_number,
                        path,
                        error,
                    )
                    skipped["count"] += 1
                    continue
                raise StreamStatsError(
                    f"Ошибка: {error}, в файле: {path}, в строке: {line_number}"
                ) from error
            yield event


def parse_file(
    path: Path, skipped: dict, skip_invalid: bool = False
) -> Iterator[dict[str, str]]:
    if path.suffix == ".csv":
        return parse_csv(path, skipped, skip_invalid)
    elif path.suffix == ".jsonl":
        return parse_jsonl(path, skipped, skip_invalid)
    else:
        raise UnsupportedFormatError("Недопустимый формат файла")
