#include <initializer_list>
#include <string>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<std::string>{
    "48656c6c6f",
};
my_data = std::vector<std::string>{
    "48656c6c6f",
};
}
