#include <initializer_list>
#include <array>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::array<double, 3>{
    1.1,
    -2.2,
    3.3,
};
}
