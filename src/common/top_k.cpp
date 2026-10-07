#include "top_k.h"

#include <queue>
#include <algorithm>
#include <functional>

struct CompareFrequency {
    bool operator()(
        const WordFrequency& a,
        const WordFrequency& b
    ) const {
        return a.frequency > b.frequency;
    }
};

std::vector<WordFrequency> getTopK(
    const FrequencyMap& frequency,
    int k
) {
    if (k <= 0) {
        return {};
    }

    std::priority_queue<WordFrequency,std::vector<WordFrequency>,CompareFrequency> minHeap;

    for (const auto& entry : frequency) {
        WordFrequency current{
            entry.first,
            entry.second
        };

        if (static_cast<int>(minHeap.size()) < k) {

            minHeap.push(current);

        } else if (
            current.frequency > minHeap.top().frequency
        ) {

            minHeap.pop();
            minHeap.push(current);
        }
    }

    std::vector<WordFrequency> result;

    while (!minHeap.empty()) {

        result.push_back(minHeap.top());

        minHeap.pop();
    }

    std::sort(
        result.begin(),
        result.end(),
        [](const WordFrequency& a,
           const WordFrequency& b) {

            if (a.frequency != b.frequency) {
                return a.frequency > b.frequency;
            }

            return a.word < b.word;
        }
    );

    return result;
}