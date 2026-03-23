#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
#include <string>
void _check() {
_Any my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
};
my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
};
}
