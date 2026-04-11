#include <initializer_list>
#include <cmath>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
Any my_data = std::vector<double>{
    INFINITY,
    -INFINITY,
    NAN,
};
my_data = std::vector<double>{
    INFINITY,
    -INFINITY,
    NAN,
};
}
