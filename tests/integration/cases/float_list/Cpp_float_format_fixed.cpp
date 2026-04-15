#include <initializer_list>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::vector<double>{
    1.100000,
    -2.200000,
    3.300000,
};
}
