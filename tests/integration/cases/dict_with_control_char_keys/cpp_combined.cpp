#include <initializer_list>
#include <cstddef>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"key\nwith\nnewlines", "value1"},
    {"key\twith\ttabs", "value2"},
};
my_data = {
    {"key\nwith\nnewlines", "value1"},
    {"key\twith\ttabs", "value2"},
};
}
