#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = {
    {{"name", "Alice"}, {"age", 30}},
    {{"name", "Bob"}, {"age", 25}},
};
}
