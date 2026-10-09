
#include "parallel_frequency.h"

#include <omp.h>
#include <stdexcept>

ParallelFrequencyMap countFrequencyParallel(
    const std::vector<std::vector<std::string>>& tokenChunks,
    int threadCount,
    const StopWordSet* stopWords,
    bool removeStopWords
) {
    if (threadCount <= 0) {
        throw std::invalid_argument(
            "Thread count must be greater than zero."
        );
    }

    std::vector<ParallelFrequencyMap> localMaps(threadCount);

    #pragma omp parallel num_threads(threadCount)
    {
        const int threadId = omp_get_thread_num();

        #pragma omp for
        for (int i = 0;
             i < static_cast<int>(tokenChunks.size());
             ++i) {

            for (const std::string& word : tokenChunks[i]) {
                if (
                    removeStopWords &&
                    stopWords != nullptr &&
                    isStopWord(word, *stopWords)
                ) {
                    continue;
                }

                ++localMaps[threadId][word];
            }
        }
    }

    // Merge the thread-local frequency maps.
    ParallelFrequencyMap globalMap;

    for (const auto& localMap : localMaps) {
        for (const auto& entry : localMap) {
            globalMap[entry.first] += entry.second;
        }
    }

    return globalMap;
}
