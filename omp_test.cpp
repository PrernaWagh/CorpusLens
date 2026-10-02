#include <iostream>
#include <omp.h>

int main()
{
    #pragma omp parallel
    {
        int id = omp_get_thread_num();
        int total = omp_get_num_threads();

        std::cout
            << "Hello from thread "
            << id
            << " of "
            << total
            << std::endl;
    }

    return 0;
}
