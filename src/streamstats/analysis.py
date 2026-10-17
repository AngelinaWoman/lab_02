from datetime import datetime
from typing import Iterator


def analyze_events(events: Iterator[dict[str, str]]) -> dict:
    total_events = 0
    level_counts = {
        "DEBUG": 0,
        "INFO": 0,
        "WARNING": 0,
        "ERROR": 0,
        "CRITICAL": 0
    }
    source_events = {}
    error_and_critical_sources = {}
    first_timestamp = None
    last_timestamp = None

    for event in events:
        total_events += 1
        if event["level"] == "DEBUG":
            level_counts["DEBUG"] += 1
        elif event["level"] == "INFO":
            level_counts["INFO"] += 1
        elif event["level"] == "WARNING":
            level_counts["WARNING"] += 1
        elif event["level"] == "ERROR":
            level_counts["ERROR"] += 1
            if event["source"] in error_and_critical_sources:
                error_and_critical_sources[event["source"]] += 1
            else:
                error_and_critical_sources[event["source"]] = 1
        elif event["level"] == "CRITICAL":
            level_counts["CRITICAL"] += 1
            if event["source"] in error_and_critical_sources:
                error_and_critical_sources[event["source"]] += 1
            else:
                error_and_critical_sources[event["source"]] = 1

        if event["source"] in source_events:
            source_events[event["source"]] += 1
        else:
            source_events[event["source"]] = 1

        current_timestamp = datetime.fromisoformat(event["timestamp"])

        if first_timestamp is None:
            first_timestamp = current_timestamp
            last_timestamp = first_timestamp
        if current_timestamp < first_timestamp:
            first_timestamp = current_timestamp
        if current_timestamp > last_timestamp:
            last_timestamp = current_timestamp

    top_error_critical_sources = sorted(error_and_critical_sources.items(), key=lambda item: item[1], reverse=True)[:5]
    
    return {
        "total_events": total_events,
        "level_counts": level_counts,
        "source_events": source_events,
        "top_error_critical_sources": top_error_critical_sources,
        "first_timestamp": first_timestamp.isoformat() if first_timestamp is not None else None,
        "last_timestamp": last_timestamp.isoformat() if last_timestamp is not None else None
    }