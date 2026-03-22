#include <cstddef>
#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
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
