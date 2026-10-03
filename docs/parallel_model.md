# Parallel Programming Model

## Selected Model

The project uses OpenMP for parallel processing.

## Why OpenMP?

The corpus analysis is performed on a shared-memory multicore
machine. The frequency-counting stage can be divided among
multiple threads because different portions of the tokenized
corpus can be processed independently.

Each OpenMP thread maintains its own local frequency map.
After parallel processing is complete, the local maps are merged
into a global frequency map.

## Parallel Structure


The processing is conceptually:

Input corpus
    |
    v
Tokenized chunks
    |
    +-------- Thread 0 -> Local frequency map
    |
    +-------- Thread 1 -> Local frequency map
    |
    +-------- Thread 2 -> Local frequency map
    |
    +-------- Thread 3 -> Local frequency map
    |
    v
Merge local maps
    |
    v
Global frequency map

## Why not MPI?

MPI is primarily useful when computation is distributed across
multiple processes or multiple machines. This project is designed
to run on a shared-memory multicore system, so OpenMP provides a
simpler model for thread-level parallelism.

## Why not CUDA?

The project does not require large-scale GPU-style numerical
computation. The workload involves strings, tokenization and
hash-map operations, which are not a natural fit for a simple
CUDA implementation.

## Thread Safety

A shared frequency map is not directly updated by all threads.
Instead, each thread uses a private/local frequency map.

This avoids concurrent modifications to the same unordered_map.

After the parallel region, the local maps are merged into the
global frequency map.

## Correctness

The parallel implementation is verified against the sequential
implementation by comparing:

- Total lines
- Total paragraphs
- Total words
- Unique words
- Total characters
- Total sentences
- Average statistics
- Top-K word frequencies
