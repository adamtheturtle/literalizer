#include <initializer_list>
#include <cstddef>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
my_data = {
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
}
