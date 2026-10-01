#ifndef RESULT_PRINTER_H
#define RESULT_PRINTER_H

#include "statistics.h"
#include "top_k.h"

void printStatistics(
    const CorpusStatistics& stats
);

void printTopK(
    const std::vector<WordFrequency>& topWords
);

#endif