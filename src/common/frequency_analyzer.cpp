#include "frequency_analyzer.h"

FrequencyMap countWordFrequency(
    const std::vector<std::string>& tokens
) {
    FrequencyMap frequency;

    for (const std::string& token : tokens) {
        ++frequency[token];
    }

    return frequency;
}