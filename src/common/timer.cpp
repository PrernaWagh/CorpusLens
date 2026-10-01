#include "timer.h"

void Timer::start()
{
    startTime =
        std::chrono::high_resolution_clock::now();
}

double Timer::stop()
{
    auto endTime =
        std::chrono::high_resolution_clock::now();

    std::chrono::duration<double> elapsed =
        endTime - startTime;

    return elapsed.count();
}