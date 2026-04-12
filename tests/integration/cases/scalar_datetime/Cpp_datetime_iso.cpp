#include <initializer_list>
#include <string>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = "2024-01-15T12:30:00+00:00";
}
