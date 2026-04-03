#include <initializer_list>
#include <cmath>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<double>{
    INFINITY,
    -INFINITY,
    NAN,
};
my_data = std::vector<double>{
    INFINITY,
    -INFINITY,
    NAN,
};
}
