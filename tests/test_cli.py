import json
import subprocess
import sys


def test_cli_multiple_files(tmp_path):
    file1 = tmp_path / "first.jsonl"
    file2 = tmp_path / "second.jsonl"
    output = tmp_path / "report.json"

    event1 = {
        "timestamp": "2026-10-18T10:00:00",
        "level": "INFO",
        "source": "app1",
        "message": "Started",
    }

    event2 = {
        "timestamp": "2026-10-18T11:00:00",
        "level": "ERROR",
        "source": "app2",
        "message": "Failed",
    }

    file1.write_text(
        json.dumps(event1) + "\n",
        encoding="utf-8",
    )
    file2.write_text(
        json.dumps(event2) + "\n",
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(file1),
            str(file2),
            "--format",
            "jsonl",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()

    report = json.loads(output.read_text(encoding="utf-8"))

    assert report["total_events"] == 2
    assert report["level_counts"]["INFO"] == 1
    assert report["level_counts"]["ERROR"] == 1
    assert report["source_events"]["app1"] == 1
    assert report["source_events"]["app2"] == 1


def test_cli_integration_with_temporary_directory(tmp_path):
    input_dir = tmp_path / "input"
    input_dir.mkdir()

    file_path = input_dir / "events.jsonl"
    output = tmp_path / "report.json"

    events = [
        {
            "timestamp": "2026-10-18T10:00:00",
            "level": "INFO",
            "source": "приложение",
            "message": "Запуск",
        },
        {
            "timestamp": "2026-10-18T10:05:00",
            "level": "WARNING",
            "source": "приложение",
            "message": "Предупреждение",
        },
    ]

    file_path.write_text(
        "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events),
        encoding="utf-8",
    )

    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "streamstats",
            "analyze",
            str(file_path),
            "--format",
            "jsonl",
            "--output",
            str(output),
        ],
        capture_output=True,
        text=True,
        check=False,
        encoding="utf-8",
        cwd=tmp_path,
        env=None,
    )

    assert result.returncode == 0, result.stderr
    assert output.exists()

    report = json.loads(output.read_text(encoding="utf-8"))

    assert report["total_events"] == 2
    assert report["level_counts"]["INFO"] == 1
    assert report["level_counts"]["WARNING"] == 1
    assert report["source_events"]["приложение"] == 2
