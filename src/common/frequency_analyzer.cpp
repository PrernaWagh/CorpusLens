
#include "frequency_analyzer.h"

FrequencyMap countWordFrequency(
    const std::vector<std::string>& tokens,
    const StopWordSet* stopWords,
    bool removeStopWords
)
{
    FrequencyMap frequency;

    for (const std::string& token : tokens) {
        if (
            removeStopWords &&
            stopWords != nullptr &&
            isStopWord(token, *stopWords)
        ) {
            continue;
        }

        ++frequency[token];
    }

    return frequency;
}
