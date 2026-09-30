#include "tokenizer.h"

#include <cctype>
#include <sstream>

using namespace std;

vector<string> tokenize(const string& line) {

    string cleaned;

    for (char ch : line) {

        if (isalnum(static_cast<unsigned char>(ch))) {
            cleaned += static_cast<char>(
                tolower(static_cast<unsigned char>(ch))
            );
        }
        else {
            cleaned += ' ';
        }
    }

    vector<string> words;
    string word;

    stringstream ss(cleaned);

    while (ss >> word) {
        words.push_back(word);
    }

    return words;
}