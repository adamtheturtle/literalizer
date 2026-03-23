#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
#include <string>
#include <cstddef>
#include <vector>
void _check() {
_Any my_data = {
    1,
    "hello",
    true,
    nullptr,
};
my_data = {
    1,
    "hello",
    true,
    nullptr,
};
}
