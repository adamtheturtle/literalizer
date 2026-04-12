#include <initializer_list>
#include <cmath>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<double>{
    INFINITY,
    -INFINITY,
    NAN,
};
}
