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
    std::vector<double>{1.5, 2.5},
    std::vector<double>{3.5, 4.5},
};
my_data = std::vector<std::vector<double>>{
    std::vector<double>{1.5, 2.5},
    std::vector<double>{3.5, 4.5},
};
}
