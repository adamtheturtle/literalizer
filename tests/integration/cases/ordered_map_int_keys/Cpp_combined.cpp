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
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
my_data = {
    {"1", "one"},
    {"2", "two"},
    {"42", "answer"},
};
}
