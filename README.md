# Потоковый анализатор файлов

## Описание

Пакет Python для потокового анализа файлов в форматах CSV и JSONL.

## Возможности

- Подсчёт общего количества событий.
- Подсчёт событий по уровням логирования.
- Подсчёт событий по источникам.
- Определение пяти источников с наибольшим количеством событий уровней ERROR и CRITICAL.
- Определение времени первого и последнего события.
- Объединение статистики из нескольких файлов.
- Проверка корректности входных данных.
- Обработка некорректных строк с возможностью остановки анализа или пропуска.
- Подсчёт количества пропущенных строк.
- Сохранение отчёта в формате JSON.

## Установка

Создать виртуальное окружение:

```bash
python -m venv .venv
```

Активировать виртуальное окружение.

Для Linux и WSL:

```bash
source .venv/bin/activate
```

Для Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

Установить проект:

```bash
python -m pip install -e .
```

Установить инструменты для тестирования и проверки кода:

```bash
python -m pip install pytest ruff
```

## Формат входных данных

Каждое событие должно содержать четыре поля:

| Поле | Описание |
|---|---|
| `timestamp` | Дата и время в формате ISO |
| `level` | Уровень логирования |
| `source` | Непустая строка с названием источника |
| `message` | Сообщение в виде строки |

Допустимые уровни логирования: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`.

### JSONL

В JSONL-файле каждое событие записывается отдельной строкой в формате JSON:

```json
{"timestamp": "2026-10-18T10:00:00", "level": "INFO", "source": "server", "message": "Сервер запущен"}
{"timestamp": "2026-10-18T10:01:00", "level": "ERROR", "source": "database", "message": "Ошибка подключения"}
```

### CSV

Первая строка CSV-файла должна содержать заголовки столбцов:

```csv
timestamp,level,source,message
2026-10-18T10:00:00,INFO,server,Сервер запущен
2026-10-18T10:01:00,ERROR,database,Ошибка подключения
```

## Запуск программы

### Анализ JSONL-файла

```bash
python -m streamstats analyze logs.jsonl --format jsonl --output report.json
```

### Анализ CSV-файла

```bash
python -m streamstats analyze logs.csv --format csv --output report.json
```

### Анализ нескольких файлов

```bash
python -m streamstats analyze logs1.jsonl logs2.jsonl --format jsonl --output report.json
```

При анализе нескольких файлов необходимо указывать один формат для всех входных файлов.

### Пропуск некорректных строк

```bash
python -m streamstats analyze logs.jsonl --format jsonl --output report.json --skip-invalid
```

По умолчанию программа останавливает анализ при обнаружении некорректной строки и сообщает имя файла и номер строки.

Если указан параметр `--skip-invalid`, некорректные строки пропускаются, а программа выводит предупреждения и продолжает анализ. Количество пропущенных строк записывается в отчёт.

### Справка

Посмотреть доступные команды и параметры:

```bash
python -m streamstats --help
python -m streamstats analyze --help
```

## Результат работы

Результат сохраняется в JSON-файл, указанный параметром `--output`.

Отчёт содержит:

- `total_events` - общее количество событий;
- `level_counts` - количество событий каждого уровня;
- `source_events` - количество событий по источникам;
- `top_error_critical_sources` - пять источников с наибольшим количеством событий уровней ERROR и CRITICAL;
- `first_timestamp` - время первого события;
- `last_timestamp` - время последнего события;
- `skipped_lines` - количество пропущенных строк.

## Тестирование

Запустить тесты:

```bash
python -m pytest
```

Проверить код с помощью Ruff:

```bash
ruff check .
```

Отформатировать код:

```bash
ruff format .
```

## Структура проекта

```text
lab_02/
├── src/
│   └── streamstats/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models.py
│       ├── parsers.py
│       ├── analysis.py
│       ├── report.py
│       └── errors.py
├── tests/
│   ├── test_parsers.py
│   └── test_cli.py
├── pyproject.toml
└── README.md
```