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
    "a",  // note a
    "b",  // note b
};
my_data = std::vector<std::string>{
    "a",  // note a
    "b",  // note b
};
}
