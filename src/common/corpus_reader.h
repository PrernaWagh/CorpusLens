#ifndef CORPUS_READER_H
#define CORPUS_READER_H

#include <string>
#include <vector>

struct Document {
    std::string name;
    std::vector<std::string> lines;
};

std::vector<Document> readCorpus(const std::string& inputPath);

#endif
