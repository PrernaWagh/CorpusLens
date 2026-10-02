#include <iostream>
#include <omp.h>

int main()
{
    #pragma omp parallel
    {
        std::cout
            << "Hello from thread "
            << omp_get_thread_num()
            << std::endl;
    }

    std::cout
        << "Maximum threads: "
        << omp_get_max_threads()
        << std::endl;

    return 0;
}