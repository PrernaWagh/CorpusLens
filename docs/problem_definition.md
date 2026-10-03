# Problem Definition

## Problem

Develop a system capable of extracting useful statistical and
structural information from a very large text corpus.

The system must also investigate how processing time changes as
the size of the input corpus increases.

## Input

The input is a plain-text corpus.

The corpus may contain:

- Multiple lines
- Multiple paragraphs
- Multiple sentences
- Repeated words
- Large numbers of tokens

## Processing

The system performs:

1. File reading
2. Tokenization
3. Line counting
4. Paragraph counting
5. Sentence counting
6. Word counting
7. Unique-word counting
8. Character counting
9. Average-statistic calculation
10. Word-frequency analysis
11. Top-K frequent-word extraction

The system provides both sequential and OpenMP-based parallel
implementations.

## Output

The system produces:

- Total lines
- Total paragraphs
- Total words
- Unique words
- Total characters
- Total sentences
- Average words per line
- Average words per sentence
- Average characters per line
- Top-K frequent words
- Execution time

## Performance Investigation

The execution time is measured for different corpus sizes and
different thread counts.

The measurements are used to calculate:

- Execution time
- Parallel speedup
- Parallel efficiency

Graphs are generated to visualize the performance behaviour.
