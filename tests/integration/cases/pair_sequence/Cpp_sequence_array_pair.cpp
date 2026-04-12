#include <initializer_list>
#include <string>
#include <array>
namespace {
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::array<std::string, 2>{
    "1",
    "hello",
};
}
