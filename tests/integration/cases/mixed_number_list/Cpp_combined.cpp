#include <initializer_list>
#include <vector>
void _check() {
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
_Any my_data = std::vector<double>{
    1,
    2.5,
    3,
};
my_data = std::vector<double>{
    1,
    2.5,
    3,
};
}
