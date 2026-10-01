#ifndef STATISTICS_H
#define STATISTICS_H

#include <cstddef>

struct CorpusStatistics {
    long long totalWords = 0;
    long long uniqueWords = 0;
    long long totalCharacters = 0;
    long long totalLines = 0;
    long long totalSentences = 0;
};

#endif