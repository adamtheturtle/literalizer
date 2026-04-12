#include <initializer_list>
#include <string>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
};
my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
};
}
