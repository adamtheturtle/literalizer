#include <string>
#include <map>
#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
my_data = {
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
}
