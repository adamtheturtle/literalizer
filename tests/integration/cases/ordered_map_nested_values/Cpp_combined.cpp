#include <initializer_list>
#include <string>
#include <map>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"name", "Alice"},
    {"scores", std::map<std::string, std::string>{{"1", "first"}, {"2", "second"}}},
};
my_data = {
    {"name", "Alice"},
    {"scores", std::map<std::string, std::string>{{"1", "first"}, {"2", "second"}}},
};
}
