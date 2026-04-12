#include <initializer_list>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions,bugprone-forwarding-reference-overload)
    Any(std::initializer_list<Any> /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
}  // namespace
static void check_() {
Any my_data = std::vector<double>{
    0.0,
    1.0,
    1500.0,
    0.001,
};
my_data = std::vector<double>{
    0.0,
    1.0,
    1500.0,
    0.001,
};
}
