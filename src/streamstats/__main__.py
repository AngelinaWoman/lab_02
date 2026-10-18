import argparse
from streamstats.analysis import analyze_events
from streamstats.parsers import parse_file
from streamstats.report import save_report
from itertools import chain
from pathlib import Path
import sys
from streamstats.errors import StreamStatsError


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m streamstats",
        description="Потоковый анализатор файлов"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze_parser = subparsers.add_parser("analyze", help="Анализировать файлы")

    analyze_parser.add_argument("inputs", nargs="+", help="Пути к входным файлам")
    analyze_parser.add_argument("--format", choices=["csv", "jsonl"], required=True, help="Формат входных файлов")
    analyze_parser.add_argument("--output", required=True, help="Путь для сохранения отчёта")
    analyze_parser.add_argument("--skip-invalid", action="store_true", help="Пропускать некорректные строки вместо остановки анализа")

    return parser

def main() -> None:
    args = build_parser().parse_args()

    try:
        events = chain.from_iterable(parse_file(Path(file_path), args.skip_invalid) for file_path in args.inputs)

        result = analyze_events(events)
        save_report(result, args.output)
    except StreamStatsError as error:
        print(error, file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()