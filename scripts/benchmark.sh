
#!/bin/bash

# ============================================================
# CorpusLens Parallel Benchmark
# ============================================================

set -e

INPUT="${1:-data/test.txt}"

THREADS=(1 2 4 8)

REPEATS=3

OUTPUT="results/parallel_results.csv"

mkdir -p results

echo "========================================"
echo "       CORPUSLENS BENCHMARK"
echo "========================================"

echo "Input file : $INPUT"
echo "Repeats    : $REPEATS"

echo

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
# Check input
# ------------------------------------------------------------

if [ ! -f "$INPUT" ]; then

    echo "ERROR: Input file not found:"
    echo "$INPUT"

    exit 1
fi

# ------------------------------------------------------------
# CSV header
# ------------------------------------------------------------

echo "input_file,input_size_bytes,threads,run,time_seconds" \
    > "$OUTPUT"

INPUT_SIZE=$(stat -c%s "$INPUT")

# ------------------------------------------------------------
# Benchmark
# ------------------------------------------------------------

for threads in "${THREADS[@]}"
do

    echo "----------------------------------------"

    echo "Threads: $threads"

    for run in $(seq 1 $REPEATS)
    do

        echo -n "Run $run: "

        RESULT=$(./parallel "$INPUT" "$threads")

        TIME=$(echo "$RESULT" |
            grep "Execution time" |
            awk '{print $4}')

        if [ -z "$TIME" ]; then

            echo "FAILED"

            exit 1
        fi

        echo "${INPUT},${INPUT_SIZE},${threads},${run},${TIME}" \
            >> "$OUTPUT"

        echo "${TIME} seconds"

    done

done

echo
echo "========================================"
echo "Benchmark completed"
echo "========================================"

echo
echo "Results saved to:"
echo "$OUTPUT"

echo
cat "$OUTPUT"
