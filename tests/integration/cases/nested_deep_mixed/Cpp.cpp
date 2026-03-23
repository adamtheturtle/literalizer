#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
#include <string>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    {std::vector<int>{1, 2}, std::vector<std::string>{"a", "b"}},
};
}
