#include <initializer_list>
#include <string>
#include <cstddef>
#include <map>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = {
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
my_data = {
    {"name", "Alice"},
    {"score", nullptr},
    {"age", 30},
};
}
