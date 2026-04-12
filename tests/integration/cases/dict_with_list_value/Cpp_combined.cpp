#include <initializer_list>
#include <string>
#include <map>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = {
    {"name", "Alice"},
    {"scores", std::vector<int>{10, 20, 30}},
};
my_data = {
    {"name", "Alice"},
    {"scores", std::vector<int>{10, 20, 30}},
};
}
