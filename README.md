# Event data pipeline

Install dependencies and build the derived data from a fresh clone:

```sh
uv sync
uv run dvc repro
```

The raw input, `data/raw/events.csv`, is tracked in Git. DVC manages the
derived CSV files locally. No DVC remote or `dvc pull` is needed.

The pipeline runs three stages:

- `clean` drops incomplete rows, invalid event types, and non-positive durations.
  Valid types are `click`, `login`, `purchase`, `scroll`, and `view`. It normalizes
  timestamps to `YYYY-MM-DDTHH:MM:SS` and keeps durations as whole seconds.
- `transform` adds the timestamp's date as `YYYY-MM-DD`.
- `features` adds `duration_minutes` and the full weekday name, preserving all rows.

Outputs are `data/clean/events.csv`, `data/transformed/events.csv`, and
`data/features/events.csv`. DVC tracks the scripts and inputs for each stage
and rebuilds affected outputs when they change.

Open the event duration histogram:

```sh
uv run marimo edit notebooks/report.py
```

Run the pipeline checks:

```sh
uv run python -m unittest discover -s tests
```

Submit `repo_url.txt` to the autograder.
