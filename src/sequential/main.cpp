#include <iostream>
#include <fstream>
#include <string>
#include <vector>

#include "../common/tokenizer.h"
#include "../common/frequency_analyzer.h"
#include "../common/top_k.h"
#include "../common/statistics.h"
#include "../common/timer.h"
#include "../common/result_printer.h"

int main(int argc, char* argv[])
{
    if (argc < 2) {

        std::cerr
            << "Usage: "
            << argv[0]
            << " <input_file>\n";

        return 1;
    }

    const std::string filename = argv[1];

    const int K = 10;

    std::ifstream file(filename);

    if (!file.is_open()) {

        std::cerr
            << "Error: Could not open file: "
            << filename
            << '\n';

        return 1;
    }

    CorpusStatistics stats;

    std::vector<std::string> allTokens;

    bool insideParagraph = false;

    Timer timer;

    timer.start();

    std::string line;

    while (std::getline(file, line)) {

        // -----------------------------
        // Line statistics
        // -----------------------------

        ++stats.totalLines;

        stats.totalCharacters += line.length();

        // -----------------------------
        // Paragraph detection
        // -----------------------------

        if (line.empty()) {

            if (insideParagraph) {

                ++stats.totalParagraphs;

                insideParagraph = false;
            }

        } else {

            insideParagraph = true;
        }

        // -----------------------------
        // Sentence detection
        // -----------------------------

        for (char ch : line) {

            if (
                ch == '.' ||
                ch == '?' ||
                ch == '!'
            ) {
                ++stats.totalSentences;
            }
        }

        // -----------------------------
        // Tokenization
        // -----------------------------

        std::vector<std::string> tokens =
            tokenize(line);

        stats.totalWords += tokens.size();

        allTokens.insert(
            allTokens.end(),
            tokens.begin(),
            tokens.end()
        );
    }

    // Last paragraph
    if (insideParagraph) {
        ++stats.totalParagraphs;
    }

    file.close();

    // -----------------------------
    // Word frequency
    // -----------------------------

    FrequencyMap frequency =
        countWordFrequency(allTokens);

    stats.uniqueWords =
        frequency.size();

    // -----------------------------
    // Calculate averages
    // -----------------------------

    calculateAverages(stats);

    // -----------------------------
    // Top-K
    // -----------------------------

    std::vector<WordFrequency> topWords =
        getTopK(frequency, K);

    // -----------------------------
    // Stop timer
    // -----------------------------

    double executionTime =
        timer.stop();

    // -----------------------------
    // Print results
    // -----------------------------

    printStatistics(stats);

    printTopK(topWords);

    std::cout
        << "\n========================================\n";

    std::cout
        << "Execution time : "
        << executionTime
        << " seconds\n";

    std::cout
        << "========================================\n";

    return 0;
}