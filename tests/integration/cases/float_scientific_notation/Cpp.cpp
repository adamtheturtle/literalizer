#include <initializer_list>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::vector<double>{
    0.0,
    1.0,
    1500.0,
    0.001,
};
}
