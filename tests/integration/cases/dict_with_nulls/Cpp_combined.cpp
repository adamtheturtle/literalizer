#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
void _check() {
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
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
