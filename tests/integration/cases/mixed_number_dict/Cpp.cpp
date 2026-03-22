#include <map>
#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = std::map<std::string, double>{
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
}
