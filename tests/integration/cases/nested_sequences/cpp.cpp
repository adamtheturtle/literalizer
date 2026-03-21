#include <initializer_list>
#include <cstddef>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = std::vector<std::vector<std::vector<int>>>{
    std::vector<std::vector<int>>{std::vector<int>{1, 2}, std::vector<int>{3, 4}},
    std::vector<std::vector<int>>{std::vector<int>{5}},
};
}
