#include <initializer_list>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<int>{
    0,
    1,
    -1,
};
my_data = std::vector<int>{
    0,
    1,
    -1,
};
}
