#include <initializer_list>
#include <string>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions,bugprone-forwarding-reference-overload)
    Any(std::initializer_list<Any> /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
}  // namespace
static void check_() {
Any my_data = {
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
my_data = {
    // before apple
    "apple",
    "banana",  // banana inline
    // trailing
};
}
