#include <initializer_list>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<std::vector<double>>{
    std::vector<double>{1.500000, 2.500000},
    std::vector<double>{3.500000, 4.500000},
};
}
