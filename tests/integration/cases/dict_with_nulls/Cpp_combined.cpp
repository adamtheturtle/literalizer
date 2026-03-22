#include <string>
#include <cstddef>
#include <map>
#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
my_data = {
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
}
