#include <iostream>
#include <string>
#include <vector>
#include <cstdlib>
#include <exception>

#include <omp.h>

#include "../common/corpus_reader.h"
#include "../common/stopwords.h"
#include "../common/tokenizer.h"
#include "../common/top_k.h"
#include "../common/statistics.h"
#include "../common/timer.h"
#include "../common/result_printer.h"

#include "parallel_frequency.h"

int main(int argc, char* argv[]) {
    if (argc < 3 || argc > 4) {
        std::cerr << "Usage: " << argv[0]
                  << " <input_file_or_directory> <threads>"
                  << " [--remove-stopwords]\n";
        return 1;
    }

    const std::string inputPath = argv[1];
    const int threadCount = std::atoi(argv[2]);

    if (threadCount <= 0) {
        std::cerr << "Invalid thread count.\n";
        return 1;
    }

    const bool removeStopWords =
        argc == 4 && std::string(argv[3]) == "--remove-stopwords";

    if (argc == 4 && !removeStopWords) {
        std::cerr << "Unknown option: " << argv[3] << '\n';
        return 1;
    }

    Timer timer;
    timer.start();

    std::vector<Document> documents;

    try {
        documents = readCorpus(inputPath);
    } catch (const std::exception& error) {
        std::cerr << "Corpus error: " << error.what() << '\n';
        return 1;
    }

    CorpusStatistics stats;
    std::vector<std::vector<std::string>> tokenChunks;
    std::vector<std::size_t> documentWordCounts;

    for (const Document& document : documents) {
        std::size_t documentWords = 0;
        bool insideParagraph = false;

        for (const std::string& line : document.lines) {
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
                if (ch == '.' || ch == '?' || ch == '!') {
                    ++stats.totalSentences;
                }
            }

            std::vector<std::string> tokens = tokenize(line);
            documentWords += tokens.size();
            stats.totalWords += tokens.size();
            tokenChunks.push_back(std::move(tokens));
        }

        if (insideParagraph) {
            ++stats.totalParagraphs;
        }

        documentWordCounts.push_back(documentWords);
    }

    StopWordSet stopWords;

    try {
        stopWords = loadStopWords("data/stopwords.txt");
    } catch (const std::exception& error) {
        std::cerr << error.what() << '\n';
        return 1;
    }

    ParallelFrequencyMap frequency = countFrequencyParallel(
        tokenChunks, threadCount, &stopWords, removeStopWords
    );

    stats.uniqueWords = frequency.size();
    calculateAverages(stats);

    std::vector<WordFrequency> topWords = getTopK(frequency, 10);
    double executionTime = timer.stop();

    std::cout << "\n========== DOCUMENT SUMMARY ==========\n";
    std::cout << "Documents processed: " << documents.size() << '\n';

    std::size_t totalDocumentWords = 0;
    for (std::size_t i = 0; i < documents.size(); ++i) {
        std::cout << documents[i].name << " : "
                  << documentWordCounts[i] << " words\n";
        totalDocumentWords += documentWordCounts[i];
    }

    double averageDocumentWords =
        documents.empty() ? 0.0 :
        static_cast<double>(totalDocumentWords) / documents.size();

    std::cout << "Average words per document: "
              << averageDocumentWords << '\n';

    printStatistics(stats);
    printTopK(topWords);

    std::cout << "\nThreads: " << threadCount << '\n';
    std::cout << "Execution time: "
              << executionTime << " seconds\n";

    return 0;
}
