#include <initializer_list>
#include <string>
#include <array>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::array<std::string, 3>{
    "1",
    "hello",
    "True",
};
}
