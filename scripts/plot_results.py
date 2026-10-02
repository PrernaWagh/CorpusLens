import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt


INPUT_FILE = "results/metrics.csv"

OUTPUT_DIR = "results/plots"

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


data = defaultdict(list)


with open(
    INPUT_FILE,
    "r"
) as file:

    reader = csv.DictReader(file)

    for row in reader:

        input_file = row["input_file"]

        data[input_file].append({
            "threads":
                int(row["threads"]),

            "time":
                float(row["time_seconds"]),

            "speedup":
                float(row["speedup"]),

            "efficiency":
                float(
                    row["efficiency_percent"]
                ),

            "size":
                row["input_size_mb"]
        })


# ==================================================
# 1. Execution time vs threads
# ==================================================

for input_file, rows in data.items():

    threads = [
        row["threads"]
        for row in rows
    ]

    times = [
        row["time"]
        for row in rows
    ]

    plt.figure()

    plt.plot(
        threads,
        times,
        marker="o"
    )

    plt.xlabel(
        "Number of Threads"
    )

    plt.ylabel(
        "Execution Time (seconds)"
    )

    plt.title(
        f"Execution Time vs Threads\n"
        f"{input_file}"
    )

    plt.xticks(threads)

    plt.grid(True)

    safe_name = (
        input_file
        .replace("/", "_")
        .replace(".txt", "")
    )

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"execution_time_{safe_name}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==================================================
# 2. Speedup vs threads
# ==================================================

for input_file, rows in data.items():

    threads = [
        row["threads"]
        for row in rows
    ]

    speedups = [
        row["speedup"]
        for row in rows
    ]

    plt.figure()

    plt.plot(
        threads,
        speedups,
        marker="o"
    )

    plt.xlabel(
        "Number of Threads"
    )

    plt.ylabel(
        "Speedup"
    )

    plt.title(
        f"Speedup vs Threads\n"
        f"{input_file}"
    )

    plt.xticks(threads)

    plt.grid(True)

    safe_name = (
        input_file
        .replace("/", "_")
        .replace(".txt", "")
    )

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"speedup_{safe_name}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==================================================
# 3. Efficiency vs threads
# ==================================================

for input_file, rows in data.items():

    threads = [
        row["threads"]
        for row in rows
    ]

    efficiencies = [
        row["efficiency"]
        for row in rows
    ]

    plt.figure()

    plt.plot(
        threads,
        efficiencies,
        marker="o"
    )

    plt.xlabel(
        "Number of Threads"
    )

    plt.ylabel(
        "Efficiency (%)"
    )

    plt.title(
        f"Parallel Efficiency vs Threads\n"
        f"{input_file}"
    )

    plt.xticks(threads)

    plt.grid(True)

    safe_name = (
        input_file
        .replace("/", "_")
        .replace(".txt", "")
    )

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"efficiency_{safe_name}.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


# ==================================================
# 4. Execution time vs input size
# ==================================================

size_data = defaultdict(list)


for input_file, rows in data.items():

    if not rows:
        continue

    size = rows[0]["size"]

    if size == "test":
        continue

    size = float(size)

    for row in rows:

        size_data[row["threads"]].append({
            "size": size,
            "time": row["time"]
        })


for threads, rows in size_data.items():

    rows.sort(
        key=lambda x: x["size"]
    )

    sizes = [
        row["size"]
        for row in rows
    ]

    times = [
        row["time"]
        for row in rows
    ]

    plt.figure()

    plt.plot(
        sizes,
        times,
        marker="o"
    )

    plt.xlabel(
        "Input Size (MB)"
    )

    plt.ylabel(
        "Execution Time (seconds)"
    )

    plt.title(
        f"Execution Time vs Input Size "
        f"({threads} threads)"
    )

    plt.grid(True)

    plt.savefig(
        f"{OUTPUT_DIR}/"
        f"execution_time_vs_size_"
        f"{threads}_threads.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()


print(
    "All graphs generated successfully."
)

print(
    "Graphs saved in:",
    OUTPUT_DIR
)