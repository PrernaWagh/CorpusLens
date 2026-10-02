#!/bin/bash

INPUT="data/test.txt"
OUTPUT="results/scaling_results.csv"

mkdir -p results

echo "threads,time_seconds" > "$OUTPUT"

echo "========================================"
echo "        CORPUSLENS BENCHMARK"
echo "========================================"

for threads in 1 2 4 8
do
    echo
    echo "Running with $threads threads..."

    result=$(./parallel "$INPUT" "$threads")

    time=$(echo "$result" |
        grep "Execution time" |
        awk '{print $4}')

    echo "$threads,$time" >> "$OUTPUT"

    echo "Time: $time seconds"
done

echo
echo "========================================"
echo "Benchmark completed"
echo "========================================"

cat "$OUTPUT"