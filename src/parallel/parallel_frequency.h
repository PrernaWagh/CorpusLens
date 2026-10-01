#ifndef PARALLEL_FREQUENCY_H
#define PARALLEL_FREQUENCY_H

#include <string>
#include <vector>
#include <unordered_map>

using ParallelFrequencyMap =
    std::unordered_map<std::string, long long>;

ParallelFrequencyMap countFrequencyParallel(
    const std::vector<std::vector<std::string>>& tokenChunks,
    int threadCount
);

#endif