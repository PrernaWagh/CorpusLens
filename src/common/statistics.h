#ifndef STATISTICS_H
#define STATISTICS_H

struct CorpusStatistics {

    long long totalLines = 0;

    long long totalWords = 0;

    long long uniqueWords = 0;

    long long totalCharacters = 0;

    long long totalSentences = 0;

    long long totalParagraphs = 0;

    double averageWordsPerLine = 0.0;

    double averageWordsPerSentence = 0.0;

    double averageCharactersPerLine = 0.0;
};

void calculateAverages(CorpusStatistics& stats);

#endif