#include <initializer_list>
#include <string>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = "hello # world"  // note;
my_data = "hello # world"  // note;
}
