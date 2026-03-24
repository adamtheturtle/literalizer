#include <initializer_list>
#include <string>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
"2024-01-15T18:00:00+05:30"
}
