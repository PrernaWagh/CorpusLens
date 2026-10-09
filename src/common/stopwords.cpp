
#include "stopwords.h"

#include <cctype>
#include <fstream>
#include <stdexcept>

StopWordSet loadStopWords(const std::string& filename)
{
    std::ifstream file(filename);

    if (!file.is_open()) {
        throw std::runtime_error(
            "Could not open stop-word file: " + filename
        );
    }

    StopWordSet stopWords;
    std::string word;

    while (std::getline(file, word)) {
        // Normalize words to lowercase and remove surrounding whitespace.
        std::string normalized;

        for (unsigned char ch : word) {
            if (!std::isspace(ch)) {
                normalized += static_cast<char>(std::tolower(ch));
            }
        }

        if (!normalized.empty() && normalized[0] != '#') {
            stopWords.insert(normalized);
        }
    }

    return stopWords;
}

bool isStopWord(
    const std::string& word,
    const StopWordSet& stopWords
)
{
    return stopWords.find(word) != stopWords.end();
}
