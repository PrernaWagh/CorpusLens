
#include "tokenizer.h"

#include <cctype>
#include <sstream>

using namespace std;

vector<string> tokenize(const string& line)
{
    string cleaned;
    cleaned.reserve(line.size());

    for (size_t i = 0; i < line.size(); ++i) {
        unsigned char ch = static_cast<unsigned char>(line[i]);

        if (isalnum(ch)) {
            cleaned += static_cast<char>(tolower(ch));
        }
        else if (
            line[i] == '\'' &&
            i > 0 &&
            i + 1 < line.size() &&
            isalnum(static_cast<unsigned char>(line[i - 1])) &&
            isalnum(static_cast<unsigned char>(line[i + 1]))
        ) {
            // Keep apostrophes occurring inside words.
            cleaned += '\'';
        }
        else {
            cleaned += ' ';
        }
    }

    vector<string> words;
    string word;
    stringstream ss(cleaned);

    while (ss >> word) {
        // Remove a trailing apostrophe if present.
        while (!word.empty() && word.back() == '\'') {
            word.pop_back();
        }

        while (!word.empty() && word.front() == '\'') {
            word.erase(word.begin());
        }

        if (!word.empty()) {
            words.push_back(word);
        }
    }

    return words;
}
