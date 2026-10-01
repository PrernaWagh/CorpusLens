#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "../common/tokenizer.h"
#include "../common/frequency_analyzer.h"
#include "../common/statistics.h"

int main() {

    const std::string filename = "data/test.txt";

    std::ifstream file(filename);

    if (!file.is_open()) {
        std::cerr << "Error: Could not open corpus.\n";
        return 1;
    }

    std::vector<std::string> allTokens;

    CorpusStatistics stats;

    std::string line;

    while (std::getline(file, line)) {

        ++stats.totalLines;

        stats.totalCharacters += line.length();

        for (char ch : line) {
            if (ch == '.' || ch == '?' || ch == '!') {
                ++stats.totalSentences;
            }
        }

        std::vector<std::string> tokens = tokenize(line);

        stats.totalWords += tokens.size();

        allTokens.insert(
            allTokens.end(),
            tokens.begin(),
            tokens.end()
        );
    }

    file.close();

    FrequencyMap frequency =
        countWordFrequency(allTokens);

    stats.uniqueWords = frequency.size();

    std::cout << "\n========== CORPUS STATISTICS ==========\n";

    std::cout << "Total lines      : "
              << stats.totalLines << '\n';

    std::cout << "Total words      : "
              << stats.totalWords << '\n';

    std::cout << "Unique words     : "
              << stats.uniqueWords << '\n';

    std::cout << "Total characters : "
              << stats.totalCharacters << '\n';

    std::cout << "Total sentences  : "
              << stats.totalSentences << '\n';

    std::cout << "\n========== WORD FREQUENCIES ==========\n";

    for (const auto& entry : frequency) {
        std::cout << entry.first
                  << " : "
                  << entry.second
                  << '\n';
    }

    return 0;
}