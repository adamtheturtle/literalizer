#include <initializer_list>
#include <cstddef>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<std::vector<double>>{
    std::vector<double>{1.5, 2.5},
    std::vector<double>{3.5, 4.5},
};
}
