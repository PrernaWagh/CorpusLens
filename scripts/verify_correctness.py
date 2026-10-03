#!/usr/bin/env python3

import subprocess
import sys
import re


def run_program(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("ERROR running:")
        print(" ".join(command))
        print(result.stderr)
        sys.exit(1)

    return result.stdout


def extract_statistics(output):
    statistics = {}

    patterns = {
        "Total lines":
            r"Total lines\s*:\s*(\d+)",

        "Total paragraphs":
            r"Total paragraphs\s*:\s*(\d+)",

        "Total words":
            r"Total words\s*:\s*(\d+)",

        "Unique words":
            r"Unique words\s*:\s*(\d+)",

        "Total characters":
            r"Total characters\s*:\s*(\d+)",

        "Total sentences":
            r"Total sentences\s*:\s*(\d+)",

        "Average words/line":
            r"Average words/line\s*:\s*([0-9.]+)",

        "Average words/sentence":
            r"Average words/sentence\s*:\s*([0-9.]+)",

        "Average characters/line":
            r"Average characters/line\s*:\s*([0-9.]+)",
    }

    for name, pattern in patterns.items():
        match = re.search(pattern, output)

        if match:
            statistics[name] = match.group(1)
        else:
            print(f"WARNING: Could not find {name}")

    return statistics


def extract_top_k(output):
    top_k = []

    in_top_k = False

    for line in output.splitlines():

        if "TOP FREQUENT WORDS" in line:
            in_top_k = True
            continue

        if "Threads" in line:
            break

        if in_top_k:
            match = re.match(
                r"\s*(\d+)\s+(\S+)\s+(\d+)",
                line
            )

            if match:
                rank = int(match.group(1))
                word = match.group(2)
                frequency = int(match.group(3))

                top_k.append(
                    (rank, word, frequency)
                )

    return top_k


def compare_values(name, sequential, parallel):

    if sequential == parallel:
        print(f"[PASS] {name}")
        return True

    print(f"[FAIL] {name}")
    print(f"       Sequential : {sequential}")
    print(f"       Parallel   : {parallel}")

    return False


def main():

    if len(sys.argv) < 2:
        print(
            "Usage: python3 scripts/verify_correctness.py "
            "<input_file> [threads]"
        )
        sys.exit(1)

    input_file = sys.argv[1]

    threads = 4

    if len(sys.argv) >= 3:
        threads = int(sys.argv[2])

    print()
    print("=" * 50)
    print("      PARALLEL CORRECTNESS VERIFICATION")
    print("=" * 50)
    print()

    print("Input file :", input_file)
    print("Threads    :", threads)
    print()

    sequential_output = run_program(
        ["./sequential", input_file]
    )

    parallel_output = run_program(
        ["./parallel", input_file, str(threads)]
    )

    sequential_stats = extract_statistics(
        sequential_output
    )

    parallel_stats = extract_statistics(
        parallel_output
    )

    print("Statistics comparison")
    print("-" * 50)

    all_passed = True

    for name in sequential_stats:

        if name not in parallel_stats:
            print(f"[FAIL] {name} missing from parallel output")
            all_passed = False
            continue

        passed = compare_values(
            name,
            sequential_stats[name],
            parallel_stats[name]
        )

        if not passed:
            all_passed = False

    print()
    print("Top-K comparison")
    print("-" * 50)

    sequential_top = extract_top_k(
        sequential_output
    )

    parallel_top = extract_top_k(
        parallel_output
    )

    if sequential_top == parallel_top:

        print("[PASS] Top-K frequencies")

    else:

        print("[FAIL] Top-K frequencies")

        print()
        print("Sequential:")
        for item in sequential_top:
            print(item)

        print()
        print("Parallel:")
        for item in parallel_top:
            print(item)

        all_passed = False

    print()
    print("=" * 50)

    if all_passed:
        print("RESULT: PASS")
        print("Parallel implementation matches")
        print("the sequential implementation.")
    else:
        print("RESULT: FAIL")
        print("Parallel implementation does not")
        print("match the sequential implementation.")

    print("=" * 50)
    print()

    sys.exit(0 if all_passed else 1)


if __name__ == "__main__":
    main()
