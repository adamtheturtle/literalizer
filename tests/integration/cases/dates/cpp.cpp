#include <initializer_list>
#include <cstddef>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = {
    {"date", "2024-01-15"},
    {"datetime", "2024-01-15T12:30:00+00:00"},
};
}
