import csv
import tempfile
import unittest
from pathlib import Path

from scripts.clean import clean
from scripts.features import features
from scripts.transform import transform


FIELDS = ["user_id", "timestamp", "event_type", "duration_seconds"]


class PipelineTests(unittest.TestCase):
    def run_pipeline(self, rows):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        root = Path(workspace.name)
        raw = root / "raw.csv"
        with raw.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(FIELDS)
            writer.writerows(rows)

        outputs = []
        source = raw
        for stage in (clean, transform, features):
            destination = root / stage.__name__ / "events.csv"
            stage(source, destination)
            with destination.open(newline="") as file:
                reader = csv.DictReader(file)
                outputs.append((reader.fieldnames, list(reader)))
            source = destination
        return outputs

    def test_filters_and_mixed_timestamps(self):
        valid = [
            ["u1", "2026-01-05T12:30:45", "click", "45"],
            ["u2", "2026-01-06T12:30:45.561", "login", "120"],
            ["u3", "2026-01-07 12:30:45", "purchase", "30"],
            ["u4", "01/08/2026 12:30:45", "scroll", "60"],
            ["u5", "2026-01-09T12:30:45", "view", "1"],
            ["u6", "2026-01-10T12:30:45", "click", "3600"],
            ["u7", "2026-01-11T12:30:45", "click", "90"],
        ]
        invalid = [
            ["u8", "2026-01-05T12:30:45", "VIEW", "60"],
            ["u9", "2026-01-05T12:30:45", "buy", "60"],
            ["u10", "2026-01-05T12:30:45", "click", "0"],
            ["u11", "2026-01-05T12:30:45", "click", "-10"],
            ["u12", "bad timestamp", "click", "60"],
            ["u13", "2026-01-05T12:30:45", "click", "bad duration"],
        ]
        for index in range(len(FIELDS)):
            row = valid[0].copy()
            row[index] = ""
            invalid.append(row)
        invalid.append([" ", "2026-01-05T12:30:45", "click", "60"])

        cleaned, transformed, featured = self.run_pipeline(valid + invalid)
        self.assertEqual(cleaned[0], FIELDS)
        self.assertEqual(transformed[0], FIELDS + ["date"])
        self.assertEqual(featured[0], FIELDS + ["date", "duration_minutes", "weekday"])
        self.assertEqual([len(output[1]) for output in (cleaned, transformed, featured)], [7, 7, 7])
        weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for index, (original, row) in enumerate(zip(valid, featured[1])):
            expected_date = f"2026-01-{index + 5:02d}"
            self.assertEqual(row["user_id"], original[0])
            self.assertEqual(row["event_type"], original[2])
            self.assertEqual(row["duration_seconds"], original[3])
            self.assertEqual(row["timestamp"], expected_date + "T12:30:45")
            self.assertEqual(row["date"], expected_date)
            self.assertAlmostEqual(float(row["duration_minutes"]), int(original[3]) / 60)
            self.assertEqual(row["weekday"], weekdays[index])

    def test_empty_input_keeps_headers(self):
        outputs = self.run_pipeline([])
        self.assertTrue(all(rows == [] for _, rows in outputs))
        self.assertEqual(outputs[-1][0], FIELDS + ["date", "duration_minutes", "weekday"])


if __name__ == "__main__":
    unittest.main()
