
#!/usr/bin/env python3

import random
import sys
from pathlib import Path


WORDS = [
    "algorithm",
    "analysis",
    "application",
    "array",
    "computation",
    "computer",
    "corpus",
    "data",
    "efficient",
    "frequency",
    "memory",
    "parallel",
    "performance",
    "program",
    "processing",
    "search",
    "software",
    "structure",
    "system",
    "thread",
    "token",
    "word",
    "optimization",
    "execution",
    "time",
]


def generate_corpus(output_file, target_size_mb):
    """
    Generate a text corpus approximately target_size_mb MB in size.
    """

    target_bytes = target_size_mb * 1024 * 1024

    output_path = Path(output_file)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    random.seed(42)

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

            sentence = " ".join(words) + ".\n"

            file.write(sentence)

            written_bytes += len(
                sentence.encode("utf-8")
            )

    actual_size = output_path.stat().st_size

    print(
        f"Generated: {output_file}"
    )

    print(
        f"Target size : {target_size_mb} MB"
    )

    print(
        f"Actual size : "
        f"{actual_size / (1024 * 1024):.2f} MB"
    )


def main():

    if len(sys.argv) != 3:

        print(
            "Usage:"
        )

        print(
            "python3 scripts/generate_corpus.py "
            "<output_file> <size_mb>"
        )

        print()

        print("Example:")

        print(
            "python3 scripts/generate_corpus.py "
            "data/corpus_50MB.txt 50"
        )

        sys.exit(1)

    output_file = sys.argv[1]

    try:
        size_mb = float(sys.argv[2])
    except ValueError:

        print("Error: size must be a number.")

        sys.exit(1)

    if size_mb <= 0:

        print("Error: size must be greater than zero.")

        sys.exit(1)

    generate_corpus(
        output_file,
        size_mb
    )


if __name__ == "__main__":
    main()

