#include <initializer_list>
#include <string>
#include <array>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = std::array<std::string, 2>{
    "1",
    "hello",
};
}
