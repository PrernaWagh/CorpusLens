#include <omp.h>
#include <iostream>

int main() {
    std::cout << "OpenMP version: "
              << _OPENMP << std::endl;
    return 0;
}
