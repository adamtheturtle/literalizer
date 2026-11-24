#include <cstdlib>
#include <iostream>

template<class A, class B>
void consume(const A& first, const B& second) {
    if (first.values.size() != 2 || second.values.size() != 1) {
        std::abort();
    }
    std::cout << "{\"names\":[\"" << first.name
              << "\",\"" << second.name
              << "\"],\"values\":[" << first.values[0] << "," << first.values[1]
              << "," << second.values[0] << "]}";
}
