#include <initializer_list>
#include <string>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<std::string>{
    "price $10",
    "$HOME",
};
my_data = std::vector<std::string>{
    "price $10",
    "$HOME",
};
}
