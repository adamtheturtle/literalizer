#include <initializer_list>
#include <string>
#include <map>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = {
    /* Server configuration */
    {"host", "localhost"},  /* default host */
    {"port", 8080},
    /* Enable debug mode */
    {"debug", true},
};
}
