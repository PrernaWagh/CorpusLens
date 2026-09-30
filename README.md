# CorpusLens

## Parallel Large-Scale Text Corpus Analysis

CorpusLens is a text analytics system designed to extract statistical
and structural information from very large text corpora.

The project compares sequential processing with parallel processing
using OpenMP and studies how execution time changes with corpus size
and number of threads.

## Current Features

- Text corpus reading
- Tokenization
- Case normalization
- Word frequency analysis
- Total word count
- Unique word count
- Character count
- Line count
- Sentence count
- Execution-time measurement

## Technologies

- C++
- OpenMP
- Python
- Git/GitHub

## Project Structure

```text
CorpusLens/
├── src/
│   ├── common/
│   ├── sequential/
│   └── parallel/
├── data/
├── tests/
├── results/
├── graphs/
├── scripts/
├── docs/
└── README.md
