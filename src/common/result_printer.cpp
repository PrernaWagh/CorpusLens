#include "result_printer.h"

#include <iostream>
#include <iomanip>

void printStatistics(
    const CorpusStatistics& stats
) {
    std::cout
        << "\n========================================\n";

    std::cout
        << "          CORPUS STATISTICS\n";

    std::cout
        << "========================================\n";

    std::cout
        << "Total lines             : "
        << stats.totalLines
        << '\n';

    std::cout
        << "Total paragraphs        : "
        << stats.totalParagraphs
        << '\n';

    std::cout
        << "Total words             : "
        << stats.totalWords
        << '\n';

    std::cout
        << "Unique words            : "
        << stats.uniqueWords
        << '\n';

    std::cout
        << "Total characters        : "
        << stats.totalCharacters
        << '\n';

    std::cout
        << "Total sentences         : "
        << stats.totalSentences
        << '\n';

    std::cout
        << std::fixed
        << std::setprecision(2);

    std::cout
        << "Average words/line      : "
        << stats.averageWordsPerLine
        << '\n';

    std::cout
        << "Average words/sentence  : "
        << stats.averageWordsPerSentence
        << '\n';

    std::cout
        << "Average characters/line : "
        << stats.averageCharactersPerLine
        << '\n';
}

void printTopK(
    const std::vector<WordFrequency>& topWords
) {
    std::cout
        << "\n========================================\n";

    std::cout
        << "          TOP FREQUENT WORDS\n";

    std::cout
        << "========================================\n";

    std::cout
        << std::left
        << std::setw(10)
        << "Rank"
        << std::setw(25)
        << "Word"
        << "Frequency\n";

    std::cout
        << "----------------------------------------\n";

    int rank = 1;

    for (const auto& item : topWords) {

        std::cout
            << std::left
            << std::setw(10)
            << rank
            << std::setw(25)
            << item.word
            << item.frequency
            << '\n';

        ++rank;
    }
}