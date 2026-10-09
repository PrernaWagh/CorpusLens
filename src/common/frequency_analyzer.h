#ifndef FREQUENCY_ANALYZER_H
#define FREQUENCY_ANALYZER_H

#include <string>
#include <vector>
#include <unordered_map>

#include "stopwords.h"

using FrequencyMap =
    std::unordered_map<std::string, long long>;

FrequencyMap countWordFrequency(
    const std::vector<std::string>& tokens,
    const StopWordSet* stopWords = nullptr,
    bool removeStopWords = false
);

#endif
