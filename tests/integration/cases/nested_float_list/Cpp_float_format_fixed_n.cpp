#include <initializer_list>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = std::vector<std::vector<double>>{
    std::vector<double>{1.500000, 2.500000},
    std::vector<double>{3.500000, 4.500000},
};
}
