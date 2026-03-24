#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"name", "Alice"},
    {"scores", std::vector<int>{10, 20, 30}},
};
my_data = {
    {"name", "Alice"},
    {"scores", std::vector<int>{10, 20, 30}},
};
}
