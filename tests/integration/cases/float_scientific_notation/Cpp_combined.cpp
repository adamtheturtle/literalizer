#include <initializer_list>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
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
