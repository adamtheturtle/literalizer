#include <initializer_list>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = std::vector<double>{
    0.000000,
    1.000000,
    1500.000000,
    0.001000,
};
}
