import csv
import json

from streamstats.parsers import parse_csv, parse_jsonl


def test_parse_jsonl(tmp_path):
    file_path = tmp_path / "events.jsonl"

    event = {
        "timestamp": "2026-10-18T10:00:00",
        "level": "INFO",
        "source": "app",
        "message": "Started",
    }

    file_path.write_text(
        json.dumps(event) + "\n",
        encoding="utf-8",
    )

    skipped = {"count": 0}
    result = list(parse_jsonl(file_path, skipped))

    assert result == [event]
    assert skipped["count"] == 0


def test_parse_csv(tmp_path):
    file_path = tmp_path / "events.csv"

    event = {
        "timestamp": "2026-10-18T10:00:00",
        "level": "INFO",
        "source": "app",
        "message": "Started",
    }

    with file_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=event.keys())
        writer.writeheader()
        writer.writerow(event)

    skipped = {"count": 0}
    result = list(parse_csv(file_path, skipped))

    assert result == [event]
    assert skipped["count"] == 0


def test_parse_empty_jsonl(tmp_path):
    file_path = tmp_path / "empty.jsonl"
    file_path.write_text("", encoding="utf-8")

    skipped = {"count": 0}
    result = list(parse_jsonl(file_path, skipped))

    assert result == []
    assert skipped["count"] == 0


def test_parse_invalid_jsonl_default_mode(tmp_path):
    from streamstats.errors import StreamStatsError

    file_path = tmp_path / "invalid.jsonl"
    file_path.write_text(
        '{"timestamp": "2026-10-18T10:00:00", '
        '"level": "INFO", "source": "app", "message": "OK"}\n'
        "{invalid json}\n",
        encoding="utf-8",
    )

    skipped = {"count": 0}

    try:
        list(parse_jsonl(file_path, skipped))
    except StreamStatsError as error:
        assert "invalid.jsonl" in str(error)
        assert "2" in str(error)
    else:
        raise AssertionError("Ожидалась ошибка для повреждённой строки")

    assert skipped["count"] == 0


def test_parse_invalid_jsonl_skip_mode(tmp_path):
    file_path = tmp_path / "invalid.jsonl"
    file_path.write_text(
        '{"timestamp": "2026-10-18T10:00:00", '
        '"level": "INFO", "source": "app", "message": "OK"}\n'
        "{invalid json}\n",
        encoding="utf-8",
    )

    skipped = {"count": 0}
    result = list(parse_jsonl(file_path, skipped, skip_invalid=True))

    assert len(result) == 1
    assert result[0]["source"] == "app"
    assert skipped["count"] == 1


def test_parse_unicode_jsonl(tmp_path):
    file_path = tmp_path / "unicode.jsonl"

    event = {
        "timestamp": "2026-10-18T10:00:00",
        "level": "INFO",
        "source": "приложение",
        "message": "Привет, мир!",
    }

    file_path.write_text(
        json.dumps(event, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    skipped = {"count": 0}
    result = list(parse_jsonl(file_path, skipped))

    assert result == [event]
    assert result[0]["message"] == "Привет, мир!"
