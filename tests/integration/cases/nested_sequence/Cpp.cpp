#include <initializer_list>
#include <string>
#include <cstddef>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = {
    true,
    "hi",
    std::vector<int>{1, 2},
    nullptr,
};
}
