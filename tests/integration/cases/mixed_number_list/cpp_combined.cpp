#include <initializer_list>
#include <cstddef>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
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
