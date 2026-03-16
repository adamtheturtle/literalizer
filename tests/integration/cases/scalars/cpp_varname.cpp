#include <initializer_list>
#include <cstddef>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
}
