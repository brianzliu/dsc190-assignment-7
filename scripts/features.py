import csv
from datetime import date
from pathlib import Path


WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")


def features(source, destination):
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    with open(source, newline="") as source_file, open(destination, "w", newline="") as output_file:
        reader = csv.DictReader(source_file)
        writer = csv.DictWriter(
            output_file, fieldnames=[*reader.fieldnames, "duration_minutes", "weekday"]
        )
        writer.writeheader()
        for row in reader:
            row["duration_minutes"] = int(row["duration_seconds"]) / 60
            row["weekday"] = WEEKDAYS[date.fromisoformat(row["date"]).weekday()]
            writer.writerow(row)


if __name__ == "__main__":
    features("data/transformed/events.csv", "data/features/events.csv")
