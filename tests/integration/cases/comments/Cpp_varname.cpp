#include <initializer_list>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
#include <string>
#include <map>
void _check() {
_Any my_data = {
    // Server configuration
    {"host", "localhost"},  // default host
    {"port", 8080},
    // Enable debug mode
    {"debug", true},
};
}
