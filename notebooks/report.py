import marimo

__generated_with = "0.25.2"
app = marimo.App()


@app.cell
def _():
    import csv
    import marimo as mo
    import matplotlib.pyplot as plt

    return csv, mo, plt


@app.cell
def _(mo):
    mo.md("""
    # Event durations

    Distribution of event durations after cleaning.
    """)
    return


@app.cell
def _(csv, mo):
    _data_path = mo.notebook_location().parent / "data" / "features" / "events.csv"
    with _data_path.open(newline="") as _file:
        duration_minutes = [float(_row["duration_minutes"]) for _row in csv.DictReader(_file)]
    return (duration_minutes,)


@app.cell
def _(duration_minutes, plt):
    _figure, _axes = plt.subplots()
    _axes.hist(duration_minutes, bins=30, edgecolor="white")
    _axes.set(title="Event duration distribution", xlabel="Duration (minutes)", ylabel="Number of events")
    _figure.tight_layout()
    _figure
    return


if __name__ == "__main__":
    app.run()
