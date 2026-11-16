import csv
from datetime import datetime
from pathlib import Path


VALID_EVENT_TYPES = {"click", "login", "purchase", "scroll", "view"}
TIMESTAMP_FORMATS = (
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
)


def normalize_timestamp(value):
    for timestamp_format in TIMESTAMP_FORMATS:
        try:
            return datetime.strptime(value, timestamp_format).isoformat(timespec="seconds")
        except ValueError:
            continue
    raise ValueError(f"Invalid timestamp: {value!r}")


def clean(source, destination):
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    with open(source, newline="") as source_file, open(destination, "w", newline="") as output_file:
        reader = csv.DictReader(source_file)
        writer = csv.DictWriter(output_file, fieldnames=reader.fieldnames)
        writer.writeheader()
        for row in reader:
            if any(value is None or not value.strip() for value in row.values()):
                continue
            if row["event_type"] not in VALID_EVENT_TYPES:
                continue
            try:
                duration = int(row["duration_seconds"])
                timestamp = normalize_timestamp(row["timestamp"])
            except ValueError:
                continue
            if duration <= 0:
                continue
            row["duration_seconds"] = duration
            row["timestamp"] = timestamp
            writer.writerow(row)


if __name__ == "__main__":
    clean("data/raw/events.csv", "data/clean/events.csv")
