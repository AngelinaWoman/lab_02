from streamstats.errors import InvalidEventError, InvalidTimestampError
from datetime import datetime

VALID_LEVELS = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}

def validate_event(event: dict) -> None:
    if not ("level" in event and "timestamp" in event and "source" in event and "message" in event):
        raise InvalidEventError("Присутствуют не все обязательные поля")
    if not (isinstance(event["level"], str) and isinstance(event["timestamp"], str) and isinstance(event["source"], str) and isinstance(event["message"], str)):
        raise InvalidEventError("Поля должны быть строками")
    if not event["source"].strip():
        raise InvalidEventError("Поле 'source' не должно быть пустым")
    if event["level"] not in VALID_LEVELS:
        raise InvalidEventError("Недопустимое значение 'level'")
    try:
        datetime.fromisoformat(event["timestamp"])
    except ValueError:
        raise InvalidTimestampError("Недопустимое значение 'timestamp'")