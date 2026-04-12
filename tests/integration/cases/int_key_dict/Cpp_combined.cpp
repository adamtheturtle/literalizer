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
Any my_data = std::map<std::string, std::string>{
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
my_data = std::map<std::string, std::string>{
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
}
