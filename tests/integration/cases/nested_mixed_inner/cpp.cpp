#include <initializer_list>
#include <cstddef>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = {
    {1, "a"},
    {2, "b"},
};
}
