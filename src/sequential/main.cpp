#include <iostream>
#include <string>
#include <vector>
#include <exception>

#include "../common/corpus_reader.h"
#include "../common/tokenizer.h"
#include "../common/frequency_analyzer.h"
#include "../common/top_k.h"
#include "../common/statistics.h"
#include "../common/timer.h"
#include "../common/result_printer.h"
#include "../common/stopwords.h"

int main(int argc, char* argv[]) {
    if (argc < 2 || argc > 3) {
        std::cerr << "Usage: " << argv[0]
                  << " <input_file_or_directory> [--remove-stopwords]\n";
        return 1;
    }

    const std::string inputPath = argv[1];
    const bool removeStopWords =
        argc == 3 && std::string(argv[2]) == "--remove-stopwords";

    if (argc == 3 && !removeStopWords) {
        std::cerr << "Unknown option: " << argv[2] << '\n';
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
    std::vector<std::string> allTokens;
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

            allTokens.insert(
                allTokens.end(), tokens.begin(), tokens.end()
            );
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

    FrequencyMap frequency = countWordFrequency(
        allTokens, &stopWords, removeStopWords
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

    std::cout << "\nExecution time: "
              << executionTime << " seconds\n";

    return 0;
}
