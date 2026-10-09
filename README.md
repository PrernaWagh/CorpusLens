# CorpusLens
## Parallel Large-Scale Text Corpus Analysis

CorpusLens is a text analytics system designed to extract useful statistical and structural information from large text corpora. It compares sequential processing with parallel processing using OpenMP and investigates how execution time changes with corpus size and number of threads.

The project combines a C++ processing engine with a Python Streamlit dashboard to make corpus analysis, performance evaluation, and result comparison easier to perform and understand.

## Objectives

- Extract statistical information from large text corpora.
- Analyse word frequencies and identify the most frequent words.
- Calculate corpus-level and document-level statistics.
- Implement sequential and OpenMP parallel processing.
- Compare execution times for different thread counts.
- Verify that sequential and parallel implementations produce consistent results.
- Study the effect of increasing corpus size on processing performance.

## Features

### Text Corpus Analysis
- Read text files and process multiple text documents.
- Tokenize text into words.
- Normalize word case for consistent frequency counting.
- Calculate total word count and unique word count.
- Calculate character, line, and sentence counts.
- Calculate average statistics supported by the implementation.
- Identify the most frequently occurring words.

### Multi-Document Processing
- Process a single text file or a directory containing multiple text files.
- Maintain document-level word counts.
- Calculate the number of documents processed.
- Calculate average words per document.
- Display individual document statistics in the dashboard.

### Stop-Word Filtering
- Support an option to enable stop-word filtering through the C++ command-line interface.
- Compare word-frequency results with and without stop-word filtering.

The exact source of the stop-word list depends on the current C++ implementation.

### Sequential and Parallel Processing
- Execute the sequential implementation as a baseline.
- Execute the parallel implementation using OpenMP.
- Configure the number of threads for parallel runs.
- Compare sequential and parallel outputs for correctness.

### Interactive Dashboard
The Streamlit dashboard provides the following sections:

- **Corpus Analysis:** View corpus statistics and document-level analytics.
- **Word Frequency:** Explore frequently occurring words.
- **Performance:** Compare execution times across processing configurations.
- **Correctness:** Compare the outputs of sequential and parallel processing.

### Performance Evaluation
- Measure execution time.
- Compare sequential and parallel processing.
- Investigate the effect of thread count on execution time.
- Study processing time as the corpus size increases.

## Technologies Used

| Technology | Purpose |
|---|---|
| C++ | Core text-processing engine |
| OpenMP | Shared-memory parallel processing |
| Python | Dashboard integration and data handling |
| Streamlit | Interactive web dashboard |
| pandas | Tabular data processing |
| Matplotlib | Visualization, where used |
| Make | Build automation |
| Git and GitHub | Version control and collaboration |

## Project Structure

```text
CorpusLens/
├── src/
│   ├── common/
│   │   ├── tokenizer.h
│   │   ├── tokenizer.cpp
│   │   ├── corpus_reader.h
│   │   ├── corpus_reader.cpp
│   │   ├── frequency.h
│   │   ├── frequency.cpp
│   │   ├── statistics.h
│   │   ├── statistics.cpp
│   │   ├── stopwords.h
│   │   ├── stopwords.cpp
│   │   ├── top_k.h
│   │   ├── top_k.cpp
│   │   ├── timer.h
│   │   └── printer.h
│   ├── sequential/
│   │   └── main.cpp
│   └── parallel/
│       ├── main.cpp
│       └── parallel_frequency.cpp
│       └── parallel_frequency.h
          
├── frontend/
│   └── app.py
├── data/
│   ├── test.txt
│   └── multi_test/
│       ├── first.txt
│       └── second.txt
├── results/
├── graphs/
├── scripts/
├── docs/
├── makefile
└── README.md
```

## System Requirements

- Linux or Windows Subsystem for Linux (WSL).
- A C++ compiler supporting C++17.
- OpenMP support in the compiler.
- Python 3.
- pip for installing Python packages.
- Git for version control.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/PrernaWagh/CorpusLens.git
cd CorpusLens
```

### 2. Compile the C++ programs

Use the build targets defined in the project's `makefile`.

```bash
make -f makefile
```

If your makefile uses a different target or requires specific dependencies, follow the commands defined in that file.

### 3. Install Python dependencies

If the repository contains a `requirements.txt` file, install its dependencies:

```bash
pip install -r requirements.txt
```

Otherwise, install the packages required by the current dashboard, for example:

```bash
pip install streamlit pandas matplotlib
```

### 4. Run the Streamlit dashboard

```bash
streamlit run frontend/app.py
```

Streamlit will provide a local URL that you can open in your browser.

## Running the C++ Programs

### Sequential execution

Analyse a single text file:

```bash
./sequential data/test.txt
```

Analyse a directory containing multiple text files:

```bash
./sequential data/multi_test
```

Enable stop-word filtering:

```bash
./sequential data/multi_test --remove-stopwords
```

### Parallel execution

Run the parallel implementation using two threads:

```bash
./parallel data/multi_test 2
```

Run it with four threads:

```bash
./parallel data/multi_test 4
```

Enable stop-word filtering:

```bash
./parallel data/multi_test 2 --remove-stopwords
```

The supported command-line arguments depend on the current executable implementation.

## Input Datasets

CorpusLens is intended to analyse text datasets such as:

- News articles.
- Movie reviews.
- Research abstracts.
- Wikipedia articles.
- Collections of plain-text documents.

A directory containing multiple `.txt` files can be used for multi-document analysis.

The dashboard may also prepare CSV rows as individual documents or extract text files from ZIP archives, depending on the implemented upload-handling functionality. For CSV input, select the column that contains the actual text rather than IDs or category labels.

For meaningful document-level analytics, each document should represent a logical text unit, such as one article or one review.

## Statistical Measures

CorpusLens calculates or is designed to report the following measures, subject to the current implementation:

| Measure | Description |
|---|---|
| Total words | Total tokens counted across the corpus |
| Unique words | Number of distinct tokens |
| Total characters | Number of characters counted by the implementation |
| Total lines | Number of lines processed |
| Total sentences | Number of sentences detected |
| Word frequency | Number of occurrences of each word |
| Top frequent words | Words with the highest occurrence counts |
| Average words per line | Counted words divided by processed lines |
| Average words per sentence | Counted words divided by detected sentences |
| Average characters per line | Counted characters divided by processed lines |
| Documents processed | Number of documents read |
| Average words per document | Counted words divided by documents processed |
| Execution time | Time taken for the measured processing operation |

Exact definitions, punctuation handling, empty-document handling, and stop-word effects should follow the implementation in the source code.

## Performance Evaluation

The sequential implementation serves as the baseline for evaluating the OpenMP implementation.

A typical experiment is:

1. Select a fixed corpus.
2. Run the sequential implementation and record its execution time.
3. Run the parallel implementation with different thread counts.
4. Repeat the experiment with larger corpus sizes.
5. Compare execution time and output correctness.
6. Plot the results to study scalability.

### Speedup

Speedup measures the improvement in execution time obtained through parallel processing.

Speedup = Sequential Execution Time / Parallel Execution Time

### Parallel Efficiency

Parallel efficiency measures how effectively the available threads are used.

**Parallel Efficiency:**

Parallel Efficiency = Sequential Execution Time / (Parallel Execution Time × Number of Threads)

For meaningful comparisons, use the same input corpus and counting configuration for sequential and parallel runs. Very small inputs may not show a speedup because thread-management overhead can outweigh the benefits of parallelism.

## Correctness Verification

Correctness testing compares the sequential and parallel implementations on the same input.

The comparison should check:

- Total word count.
- Unique word count.
- Other applicable corpus statistics.
- Word-frequency counts.
- Top frequent words.
- Document-level counts, where available.

Both implementations should use equivalent tokenization and filtering rules.

## Testing

Use the sample corpus to check basic functionality:

```bash
./sequential data/multi_test
./parallel data/multi_test 2
```

Then repeat with stop-word filtering enabled.

Test additional cases, including:

- An empty text file.
- A single-document corpus.
- A directory containing multiple documents.
- Documents with punctuation and mixed capitalization.
- Documents with repeated words.
- Larger corpora for performance testing.

## Future Enhancements

Potential extensions include:

- More robust CSV and ZIP ingestion.
- Configurable stop-word lists.
- Document-length distributions and visualizations.
- Additional text statistics.
- Automated performance reports.
- Larger benchmark datasets.
- More comprehensive automated tests.
- Improved handling of malformed and empty input files.

## Conclusion

CorpusLens combines text analytics with parallel computing to investigate the processing of large text corpora. Its sequential and OpenMP implementations provide a basis for comparing execution times and validating results, while the Streamlit dashboard makes corpus statistics and experimental results easier to explore.

The project demonstrates how parallel programming can be applied to text processing and how performance changes with corpus size and thread count.

## Author and Repository

**Project:** CorpusLens — Parallel Large-Scale Text Corpus Analysis

**Repository:** [GitHub — CorpusLens](https://github.com/PrernaWagh/CorpusLens)

**Primary technologies:** C++, OpenMP, Python and Streamlit
