#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <cstdlib>

#include <omp.h>

#include "../common/tokenizer.h"
#include "../common/top_k.h"
#include "../common/statistics.h"
#include "../common/timer.h"
#include "../common/result_printer.h"

#include "parallel_frequency.h"

int main(int argc, char* argv[])
{
    if (argc < 3) {

        std::cerr
            << "Usage: "
            << argv[0]
            << " <input_file> <threads>\n";

        return 1;
    }

    const std::string filename = argv[1];

    const int threadCount =
        std::atoi(argv[2]);

    if (threadCount <= 0) {

        std::cerr
            << "Invalid thread count.\n";

        return 1;
    }

    std::ifstream file(filename);

    if (!file.is_open()) {

        std::cerr
            << "Could not open file: "
            << filename
            << '\n';

        return 1;
    }

    std::vector<std::vector<std::string>>
        tokenChunks;

    CorpusStatistics stats;

    bool insideParagraph = false;

    std::string line;

    Timer timer;

    timer.start();

    while (std::getline(file, line)) {

        ++stats.totalLines;

        stats.totalCharacters += line.length();

        if (line.empty()) {

            if (insideParagraph) {

                ++stats.totalParagraphs;

                insideParagraph = false;
            }

        } else {

            insideParagraph = true;
        }

        for (char ch : line) {

            if (
                ch == '.' ||
                ch == '?' ||
                ch == '!'
            ) {
                ++stats.totalSentences;
            }
        }

        std::vector<std::string> tokens =
            tokenize(line);

        stats.totalWords += tokens.size();

        tokenChunks.push_back(
            std::move(tokens)
        );
    }

    if (insideParagraph) {
        ++stats.totalParagraphs;
    }

    file.close();

    ParallelFrequencyMap frequency =
        countFrequencyParallel(
            tokenChunks,
            threadCount
        );

    stats.uniqueWords =
        frequency.size();

    calculateAverages(stats);

    std::vector<WordFrequency> topWords =
        getTopK(frequency, 10);

    double executionTime =
        timer.stop();

    printStatistics(stats);

    printTopK(topWords);

    std::cout
        << "\nThreads         : "
        << threadCount
        << '\n';

    std::cout
        << "Execution time  : "
        << executionTime
        << " seconds\n";
    return 0;
}