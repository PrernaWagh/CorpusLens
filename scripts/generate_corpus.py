import random
import sys
from pathlib import Path


WORDS = [
    "parallel",
    "programming",
    "algorithm",
    "data",
    "structure",
    "efficient",
    "processing",
    "large",
    "corpus",
    "system",
    "performance",
    "thread",
    "memory",
    "computation",
    "analysis",
    "software",
    "optimization",
    "search",
    "frequency",
    "token",
    "openmp",
    "computer",
    "science",
    "execution",
    "runtime",
    "processor",
    "workload",
    "scalability",
    "benchmark",
    "implementation",
]


def generate_corpus(output_file, target_size_mb):

    target_bytes = target_size_mb * 1024 * 1024

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    written_bytes = 0

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as file:

        while written_bytes < target_bytes:

            sentence_length = random.randint(
                8,
                20
            )

            words = [
                random.choice(WORDS)
                for _ in range(sentence_length)
            ]

            sentence = " ".join(words)

            sentence += ".\n"

            file.write(sentence)

            written_bytes += len(
                sentence.encode("utf-8")
            )

    actual_size = output_path.stat().st_size

    print(
        f"Created: {output_file}"
    )

    print(
        f"Target: {target_size_mb} MB"
    )

    print(
        f"Actual: "
        f"{actual_size / (1024 * 1024):.2f} MB"
    )


if __name__ == "__main__":

    if len(sys.argv) != 3:

        print(
            "Usage:"
        )

        print(
            "python3 "
            "scripts/generate_corpus.py "
            "<output_file> <size_mb>"
        )

        sys.exit(1)

    output_file = sys.argv[1]

    size_mb = int(sys.argv[2])

    if size_mb <= 0:

        print("Size must be positive.")

        sys.exit(1)

    generate_corpus(
        output_file,
        size_mb
    )