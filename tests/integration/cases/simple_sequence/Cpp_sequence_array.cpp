#include <initializer_list>
#include <string>
#include <cstddef>
#include <array>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    _Any my_data = std::array<std::string, 4>{
    "1",
    "hello",
    "True",
    "None",
};
}
