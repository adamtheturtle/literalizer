#include <initializer_list>
#include <cstddef>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
    [[maybe_unused]] _Any _v = {
    // Server configuration
    {"host", "localhost"},  // default host
    {"port", 8080},
    // Enable debug mode
    {"debug", true},
};
}
