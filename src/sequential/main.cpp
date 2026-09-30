#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include <unordered_map>
#include <chrono>

#include "../common/tokenizer.h"

using namespace std;

int main() {

    string filename = "data/test.txt";

    long long totalWords = 0;
    long long totalCharacters = 0;
    long long totalLines = 0;
    long long totalSentences = 0;

    ifstream file(filename);

    if (!file.is_open()) {
        cerr << "Error: Could not open file." << endl;
        return 1;
    }

    unordered_map<string, long long> frequency;

    string line;

    // Start timer
    auto start = chrono::high_resolution_clock::now();

    while (getline(file, line)) {

        vector<string> words = tokenize(line);

        totalLines++;

        totalCharacters += line.length();

        totalWords += words.size();

        for (const string& word : words) {
            frequency[word]++;
        }

        for (char ch : line) {
            if (ch == '.' || ch == '?' || ch == '!') {
                totalSentences++;
            }
        }
    }

    // Stop timer
    auto end = chrono::high_resolution_clock::now();

    file.close();

    // Calculate execution time
    double executionTime =
        chrono::duration<double>(end - start).count();

    cout << "\n========== CORPUS STATISTICS ==========\n";

    cout << "Total lines       : " << totalLines << endl;
    cout << "Total words       : " << totalWords << endl;
    cout << "Unique words      : " << frequency.size() << endl;
    cout << "Total characters  : " << totalCharacters << endl;
    cout << "Total sentences   : " << totalSentences << endl;

    cout << "Execution time    : "
         << executionTime
         << " seconds" << endl;

    cout << "\nWord Frequencies:\n";

    for (const auto& entry : frequency) {
        cout << entry.first
             << " : "
             << entry.second
             << endl;
    }

    return 0;
}