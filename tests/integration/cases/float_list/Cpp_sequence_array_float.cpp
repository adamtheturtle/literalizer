#include <initializer_list>
#include <array>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
Any my_data = std::array<double, 3>{
    1.1,
    -2.2,
    3.3,
};
}
