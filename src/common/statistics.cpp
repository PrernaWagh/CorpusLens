#include "statistics.h"

void calculateAverages(CorpusStatistics& stats)
{
    if (stats.totalLines > 0) {

        stats.averageWordsPerLine =
            static_cast<double>(stats.totalWords)
            / stats.totalLines;

        stats.averageCharactersPerLine =
            static_cast<double>(stats.totalCharacters)
            / stats.totalLines;
    }

    if (stats.totalSentences > 0) {

        stats.averageWordsPerSentence =
            static_cast<double>(stats.totalWords)
            / stats.totalSentences;
    }
}