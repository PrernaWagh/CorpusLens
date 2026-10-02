
#!/usr/bin/env python3

import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt


INPUT_FILE = "results/scaling_results.csv"

OUTPUT_DIR = "results/plots"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ============================================================
# Read CSV
# ============================================================

data = defaultdict(list)

with open(
    INPUT_FILE,
    "r",
    newline=""
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        input_file = row["input_file"]

        size_mb = float(
            row["input_size_mb"]
        )

        threads = int(
            row["threads"]
        )

        time = float(
            row["time_seconds"]
        )

        data[
            (input_file, size_mb, threads)
        ].append(time)


# ============================================================
# Calculate average execution time
# ============================================================

averages = {}

for key, values in data.items():

    averages[key] = (
        sum(values) / len(values)
    )


# ============================================================
# Save processed results
# ============================================================

processed_file = (
    "results/processed_results.csv"
)

with open(
    processed_file,
    "w",
    newline=""
) as file:

    writer = csv.writer(file)

    writer.writerow([
        "input_file",
        "size_mb",
        "threads",
        "average_time_seconds",
        "speedup",
        "efficiency"
    ])

    # Group by input file

    input_groups = defaultdict(dict)

    for (
        input_file,
        size_mb,
        threads
    ), time in averages.items():

        input_groups[
            (input_file, size_mb)
        ][threads] = time

    for (
        input_file,
        size_mb
    ), thread_data in sorted(
        input_groups.items()
    ):

        if 1 not in thread_data:
            continue

        baseline = thread_data[1]

        for threads, time in sorted(
            thread_data.items()
        ):

            speedup = baseline / time

            efficiency = speedup / threads

            writer.writerow([
                input_file,
                size_mb,
                threads,
                f"{time:.6f}",
                f"{speedup:.6f}",
                f"{efficiency:.6f}"
            ])


# ============================================================
# Graph 1: Execution time vs threads
# ============================================================

plt.figure()

for (
    input_file,
    size_mb
), thread_data in sorted(
    input_groups.items()
):

    x = sorted(thread_data.keys())

    y = [
        thread_data[t]
        for t in x
    ]

    label = f"{size_mb:g} MB"

    plt.plot(
        x,
        y,
        marker="o",
        label=label
    )

plt.xlabel("Number of Threads")

plt.ylabel(
    "Average Execution Time (seconds)"
)

plt.title(
    "Execution Time vs Number of Threads"
)

plt.xticks(
    sorted(
        set(
            threads
            for values in input_groups.values()
            for threads in values
        )
    )
)

plt.grid(True)

plt.legend()

plt.savefig(
    f"{OUTPUT_DIR}/execution_time_vs_threads.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Graph 2: Speedup vs threads
# ============================================================

plt.figure()

for (
    input_file,
    size_mb
), thread_data in sorted(
    input_groups.items()
):

    if 1 not in thread_data:
        continue

    baseline = thread_data[1]

    x = sorted(thread_data.keys())

    y = [
        baseline / thread_data[t]
        for t in x
    ]

    label = f"{size_mb:g} MB"

    plt.plot(
        x,
        y,
        marker="o",
        label=label
    )

plt.xlabel("Number of Threads")

plt.ylabel("Speedup")

plt.title(
    "Speedup vs Number of Threads"
)

plt.grid(True)

plt.legend()

plt.savefig(
    f"{OUTPUT_DIR}/speedup_vs_threads.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Graph 3: Efficiency vs threads
# ============================================================

plt.figure()

for (
    input_file,
    size_mb
), thread_data in sorted(
    input_groups.items()
):

    if 1 not in thread_data:
        continue

    baseline = thread_data[1]

    x = sorted(thread_data.keys())

    y = [
        (baseline / thread_data[t]) / t
        for t in x
    ]

    label = f"{size_mb:g} MB"

    plt.plot(
        x,
        y,
        marker="o",
        label=label
    )

plt.xlabel("Number of Threads")

plt.ylabel("Parallel Efficiency")

plt.title(
    "Parallel Efficiency vs Number of Threads"
)

plt.grid(True)

plt.legend()

plt.savefig(
    f"{OUTPUT_DIR}/efficiency_vs_threads.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


# ============================================================
# Graph 4: Execution time vs input size
# ============================================================

plt.figure()

size_groups = defaultdict(dict)

for (
    input_file,
    size_mb
), thread_data in input_groups.items():

    for threads, time in thread_data.items():

        size_groups[threads][
            size_mb
        ] = time


for threads, values in sorted(
    size_groups.items()
):

    x = sorted(values.keys())

    y = [
        values[size]
        for size in x
    ]

    plt.plot(
        x,
        y,
        marker="o",
        label=f"{threads} threads"
    )

plt.xlabel(
    "Input Size (MB)"
)

plt.ylabel(
    "Average Execution Time (seconds)"
)

plt.title(
    "Execution Time vs Input Size"
)

plt.grid(True)

plt.legend()

plt.savefig(
    f"{OUTPUT_DIR}/execution_time_vs_input_size.png",
    dpi=300,
    bbox_inches="tight"
)

plt.close()


print()
print("========================================")
print("       ANALYSIS COMPLETED")
print("========================================")

print()
print("Processed data:")
print(processed_file)

print()
print("Graphs:")

print(
    f"{OUTPUT_DIR}/execution_time_vs_threads.png"
)

print(
    f"{OUTPUT_DIR}/speedup_vs_threads.png"
)

print(
    f"{OUTPUT_DIR}/efficiency_vs_threads.png"
)

print(
    f"{OUTPUT_DIR}/execution_time_vs_input_size.png"
)
