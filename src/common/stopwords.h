
#ifndef STOPWORDS_H
#define STOPWORDS_H

#include <string>
#include <unordered_set>

using StopWordSet = std::unordered_set<std::string>;

// Load stop words from a text file, one word per line.
StopWordSet loadStopWords(const std::string& filename);

// Check whether a normalized word is a stop word.
bool isStopWord(
    const std::string& word,
    const StopWordSet& stopWords
);

#endif
