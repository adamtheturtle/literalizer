#include <initializer_list>
#include <string>
#include <map>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions,bugprone-forwarding-reference-overload)
    Any(std::initializer_list<Any> /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
}  // namespace
static void check_() {
Any my_data = {
    // Server configuration
    {"host", "localhost"},  // default host
    {"port", 8080},
    // Enable debug mode
    {"debug", true},
};
my_data = {
    // Server configuration
    {"host", "localhost"},  // default host
    {"port", 8080},
    // Enable debug mode
    {"debug", true},
};
}
