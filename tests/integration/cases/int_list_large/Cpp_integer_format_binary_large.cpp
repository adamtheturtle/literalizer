#include <initializer_list>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::vector<int>{
    0b11110100001001000000,
    -0b10011010010,
    0b11111111,
    -0b1010,
};
}
