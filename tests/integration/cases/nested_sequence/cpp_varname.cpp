#include <initializer_list>
#include <cstddef>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
}
