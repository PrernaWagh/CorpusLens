#ifndef FREQUENCY_ANALYZER_H
#define FREQUENCY_ANALYZER_H

#include <string>
#include <vector>
#include <unordered_map>

using FrequencyMap = std::unordered_map<std::string, long long>;

FrequencyMap countWordFrequency(
    const std::vector<std::string>& tokens
);

#endif