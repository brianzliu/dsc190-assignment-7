import csv
from datetime import datetime
from pathlib import Path


def transform(source, destination):
    Path(destination).parent.mkdir(parents=True, exist_ok=True)
    with open(source, newline="") as source_file, open(destination, "w", newline="") as output_file:
        reader = csv.DictReader(source_file)
        writer = csv.DictWriter(output_file, fieldnames=[*reader.fieldnames, "date"])
        writer.writeheader()
        for row in reader:
            row["date"] = datetime.fromisoformat(row["timestamp"]).date().isoformat()
            writer.writerow(row)


if __name__ == "__main__":
    transform("data/clean/events.csv", "data/transformed/events.csv")
