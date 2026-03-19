#include <initializer_list>
#include <cstddef>
#include <map>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = {
    std::vector<int>{1, 2},
    std::vector<std::string>{"a", "b"},
};
}
