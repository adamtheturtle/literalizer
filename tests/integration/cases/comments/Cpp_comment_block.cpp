#include <initializer_list>
#include <string>
#include <map>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = {
    /* Server configuration */
    {"host", "localhost"},  /* default host */
    {"port", 8080},
    /* Enable debug mode */
    {"debug", true},
};
}
