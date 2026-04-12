#include <initializer_list>
#include <cmath>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<double>{
    INFINITY,
    -INFINITY,
    NAN,
};
}
