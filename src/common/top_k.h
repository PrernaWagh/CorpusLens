#ifndef TOP_K_H
#define TOP_K_H

#include <string>
#include <vector>

#include "frequency_analyzer.h"

struct WordFrequency {
    std::string word;
    long long frequency;
};

std::vector<WordFrequency> getTopK(
    const FrequencyMap& frequency,
    int k
);

#endif