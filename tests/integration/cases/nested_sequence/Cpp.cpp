#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = {
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
}
