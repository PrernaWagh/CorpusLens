
#!/bin/bash

# ============================================================
# CorpusLens Input-Size + Thread-Scaling Benchmark
# ============================================================

set -e

THREADS=(1 2 4 8)

REPEATS=3

OUTPUT="results/scaling_results.csv"

mkdir -p results

echo "========================================"
echo "    CORPUSLENS SCALING BENCHMARK"
echo "========================================"

# ------------------------------------------------------------
# Check executable
# ------------------------------------------------------------

if [ ! -f "./parallel" ]; then

    echo "ERROR: ./parallel executable not found."

    echo "Run:"
    echo "    make parallel"

    exit 1
fi

# ------------------------------------------------------------
# Find corpus files
# ------------------------------------------------------------

INPUTS=(
    "data/test.txt"
    "data/corpus_5MB.txt"
    "data/corpus_50MB.txt"
    "data/corpus_100MB.txt"
)

# ------------------------------------------------------------
# CSV header
# ------------------------------------------------------------

echo "input_file,input_size_mb,threads,run,time_seconds" \
    > "$OUTPUT"

# ------------------------------------------------------------
# Benchmark
# ------------------------------------------------------------

for input in "${INPUTS[@]}"
do

    if [ ! -f "$input" ]; then

        echo
        echo "WARNING: Skipping missing file:"
        echo "$input"

        continue
    fi

    SIZE_BYTES=$(stat -c%s "$input")

    SIZE_MB=$(awk \
        "BEGIN {printf \"%.2f\", $SIZE_BYTES / 1024 / 1024}")

    echo
    echo "========================================"
    echo "Input: $input"
    echo "Size : ${SIZE_MB} MB"
    echo "========================================"

    for threads in "${THREADS[@]}"
    do

        echo
        echo "Threads: $threads"

        for run in $(seq 1 $REPEATS)
        do

            RESULT=$(./parallel "$input" "$threads")

            TIME=$(echo "$RESULT" |
                grep "Execution time" |
                awk '{print $4}')

            if [ -z "$TIME" ]; then

                echo "ERROR: Could not obtain execution time."

                exit 1
            fi

            echo \
                "${input},${SIZE_MB},${threads},${run},${TIME}" \
                >> "$OUTPUT"

            echo \
                "Run $run -> $TIME seconds"

        done

    done

done

echo
echo "========================================"
echo "Benchmark completed"
echo "========================================"

echo "Results:"
echo "$OUTPUT"

echo
cat "$OUTPUT"
