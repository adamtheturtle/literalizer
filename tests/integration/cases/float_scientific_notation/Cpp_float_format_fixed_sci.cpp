#include <initializer_list>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<double>{
    0.000000,
    1.000000,
    1500.000000,
    0.001000,
};
}
