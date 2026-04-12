#include <initializer_list>
#include <string>
#include <cstddef>
#include <array>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::array<std::string, 4>{
    "1",
    "hello",
    "True",
    "None",
};
}
