#include <initializer_list>
#include <string>
#include <array>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = std::array<std::string, 2>{
    "1",
    "hello",
};
}
