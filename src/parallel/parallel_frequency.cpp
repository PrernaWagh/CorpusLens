#include "parallel_frequency.h"

#include <omp.h>

ParallelFrequencyMap countFrequencyParallel(
    const std::vector<std::vector<std::string>>& tokenChunks,
    int threadCount
) {
    std::vector<ParallelFrequencyMap> localMaps(
        threadCount
    );

    #pragma omp parallel num_threads(threadCount)
    {
        int threadId = omp_get_thread_num();

        #pragma omp for
        for (
            int i = 0;
            i < static_cast<int>(tokenChunks.size());
            ++i
        ) {
            for (
                const std::string& word :
                tokenChunks[i]
            ) {
                ++localMaps[threadId][word];
            }
        }
    }

    ParallelFrequencyMap globalMap;

    for (const auto& localMap : localMaps) {

        for (const auto& entry : localMap) {

            globalMap[entry.first] +=
                entry.second;
        }
    }

    return globalMap;
}