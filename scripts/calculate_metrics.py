import csv
from collections import defaultdict


INPUT_FILE = "results/benchmark_results.csv"
OUTPUT_FILE = "results/metrics.csv"


rows = []


with open(
    INPUT_FILE,
    "r"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        rows.append({
            "input_file": row["input_file"],
            "input_size_mb": row["input_size_mb"],
            "mode": row["mode"],
            "threads": int(row["threads"]),
            "time_seconds": float(
                row["time_seconds"]
            )
        })


# ------------------------------------------------
# Find sequential baseline
# ------------------------------------------------

sequential_times = {}


for row in rows:

    if row["mode"] == "sequential":

        key = row["input_file"]

        sequential_times[key] = \
            row["time_seconds"]


# ------------------------------------------------
# Calculate metrics
# ------------------------------------------------

metrics = []


for row in rows:

    if row["mode"] != "parallel":
        continue

    input_file = row["input_file"]

    threads = row["threads"]

    parallel_time = row["time_seconds"]

    sequential_time = \
        sequential_times[input_file]

    speedup = (
        sequential_time /
        parallel_time
    )

    efficiency = (
        speedup / threads
    )

    metrics.append({
        "input_file": input_file,
        "input_size_mb": row["input_size_mb"],
        "threads": threads,
        "time_seconds": parallel_time,
        "sequential_time_seconds": sequential_time,
        "speedup": speedup,
        "efficiency": efficiency,
        "efficiency_percent":
            efficiency * 100
    })


# ------------------------------------------------
# Write CSV
# ------------------------------------------------

with open(
    OUTPUT_FILE,
    "w",
    newline=""
) as file:

    fieldnames = [
        "input_file",
        "input_size_mb",
        "threads",
        "time_seconds",
        "sequential_time_seconds",
        "speedup",
        "efficiency",
        "efficiency_percent"
    ]

    writer = csv.DictWriter(
        file,
        fieldnames=fieldnames
    )

    writer.writeheader()

    writer.writerows(metrics)


print(
    "Metrics written to:",
    OUTPUT_FILE
)


# ------------------------------------------------
# Print readable table
# ------------------------------------------------

print()

print(
    f"{'Input':<28}"
    f"{'Threads':<10}"
    f"{'Time':<12}"
    f"{'Speedup':<12}"
    f"{'Efficiency':<12}"
)

print("-" * 74)


for row in metrics:

    print(
        f"{row['input_file']:<28}"
        f"{row['threads']:<10}"
        f"{row['time_seconds']:<12.4f}"
        f"{row['speedup']:<12.2f}"
        f"{row['efficiency_percent']:<12.2f}%"
    )