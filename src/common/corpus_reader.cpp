#include "corpus_reader.h"

#include <algorithm>
#include <cctype>
#include <filesystem>
#include <fstream>
#include <stdexcept>

namespace fs = std::filesystem;

namespace {
    bool isTextFile(const fs::path& path) {
        std::string ext = path.extension().string();

        std::transform(
            ext.begin(), ext.end(), ext.begin(),
            [](unsigned char c) {
                return static_cast<char>(std::tolower(c));
            }
        );

        return ext == ".txt";
    }

    Document readOneFile(const fs::path& path) {
        std::ifstream file(path);

        if (!file.is_open()) {
            throw std::runtime_error(
                "Could not open document: " + path.string()
            );
        }

        Document document;
        document.name = path.filename().string();

        std::string line;
        while (std::getline(file, line)) {
            document.lines.push_back(line);
        }

        return document;
    }
}

std::vector<Document> readCorpus(const std::string& inputPath) {
    const fs::path path(inputPath);

    if (!fs::exists(path)) {
        throw std::runtime_error(
            "Input path does not exist: " + inputPath
        );
    }

    std::vector<Document> documents;

    if (fs::is_regular_file(path)) {
        // Preserve existing single-file support.
        documents.push_back(readOneFile(path));
    } else if (fs::is_directory(path)) {
        std::vector<fs::path> files;

        for (const auto& entry :
             fs::recursive_directory_iterator(path)) {
            if (entry.is_regular_file() &&
                isTextFile(entry.path())) {
                files.push_back(entry.path());
            }
        }

        // Ensure a stable document order.
        std::sort(files.begin(), files.end());

        for (const auto& filePath : files) {
            documents.push_back(readOneFile(filePath));
        }
    } else {
        throw std::runtime_error(
            "Input must be a regular file or directory: " + inputPath
        );
    }

    if (documents.empty()) {
        throw std::runtime_error(
            "No documents found at: " + inputPath +
            ". A directory must contain .txt files."
        );
    }

    return documents;
}
