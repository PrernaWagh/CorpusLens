#!/bin/bash

set -e

RESULT_FILE="results/benchmark_results.csv"

mkdir -p results
mkdir -p results/plots

echo "input_file,input_size_mb,mode,threads,time_seconds" \
    > "$RESULT_FILE"


echo "=============================================="
echo "          CORPUSLENS BENCHMARK"
echo "=============================================="

echo
echo "CPU threads available:"
nproc

echo


# ------------------------------------------------
# Function to extract execution time
# ------------------------------------------------

extract_time() {

    echo "$1" |
        grep "Execution time" |
        awk '{print $4}'
}


# ------------------------------------------------
# Sequential benchmark
# ------------------------------------------------

run_sequential() {

    INPUT=$1
    SIZE=$2

    echo
    echo "----------------------------------------------"
    echo "Sequential: $INPUT"
    echo "----------------------------------------------"

    OUTPUT=$(./sequential "$INPUT")

    TIME=$(extract_time "$OUTPUT")

    echo "$INPUT,$SIZE,sequential,1,$TIME" \
        >> "$RESULT_FILE"

    echo "$OUTPUT"
}


# ------------------------------------------------
# Parallel benchmark
# ------------------------------------------------

run_parallel() {

    INPUT=$1
    SIZE=$2

    for THREADS in 1 2 4 8
    do

        AVAILABLE=$(nproc)

        if [ "$THREADS" -gt "$AVAILABLE" ]; then
            continue
        fi

        echo
        echo "----------------------------------------------"
        echo "Parallel: $INPUT"
        echo "Threads: $THREADS"
        echo "----------------------------------------------"

        OUTPUT=$(./parallel "$INPUT" "$THREADS")

        TIME=$(extract_time "$OUTPUT")

        echo "$INPUT,$SIZE,parallel,$THREADS,$TIME" \
            >> "$RESULT_FILE"

        echo "$OUTPUT"

    done
}


# ------------------------------------------------
# Test corpus
# ------------------------------------------------

if [ -f "data/test.txt" ]; then

    run_sequential \
        "data/test.txt" \
        "test"

    for THREADS in 1 2 4 8
    do

        AVAILABLE=$(nproc)

        if [ "$THREADS" -gt "$AVAILABLE" ]; then
            continue
        fi

        OUTPUT=$(./parallel \
            "data/test.txt" \
            "$THREADS")

        TIME=$(extract_time "$OUTPUT")

        echo "data/test.txt,test,parallel,$THREADS,$TIME" \
            >> "$RESULT_FILE"

    done

fi


# ------------------------------------------------
# 5 MB
# ------------------------------------------------

if [ -f "data/corpus_5MB.txt" ]; then

    run_sequential \
        "data/corpus_5MB.txt" \
        5

    run_parallel \
        "data/corpus_5MB.txt" \
        5

fi


# ------------------------------------------------
# 50 MB
# ------------------------------------------------

if [ -f "data/corpus_50MB.txt" ]; then

    run_sequential \
        "data/corpus_50MB.txt" \
        50

    run_parallel \
        "data/corpus_50MB.txt" \
        50

fi


# ------------------------------------------------
# 100 MB
# ------------------------------------------------

if [ -f "data/corpus_100MB.txt" ]; then

    run_sequential \
        "data/corpus_100MB.txt" \
        100

    run_parallel \
        "data/corpus_100MB.txt" \
        100

fi


echo
echo "=============================================="
echo "Benchmark completed"
echo "=============================================="

echo
echo "Results saved to:"
echo "$RESULT_FILE"

echo
echo "Contents:"
cat "$RESULT_FILE"