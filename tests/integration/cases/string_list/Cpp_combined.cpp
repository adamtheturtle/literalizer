#include <initializer_list>
#include <string>
#include <vector>
void _check() {
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
_Any my_data = std::vector<std::string>{
    "foo",
    "bar",
    "baz",
};
my_data = std::vector<std::string>{
    "foo",
    "bar",
    "baz",
};
}
