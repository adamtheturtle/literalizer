#include <initializer_list>
#include <string>
void _check() {
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
_Any my_data = {
    "apple",
    "banana",
    "cherry",
};
my_data = {
    "apple",
    "banana",
    "cherry",
};
}
