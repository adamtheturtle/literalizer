#include <initializer_list>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<std::vector<double>>{
    std::vector<double>{1.500000, 2.500000},
    std::vector<double>{3.500000, 4.500000},
};
}
