#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = {
    std::vector<int>{1, 2},
    std::vector<std::string>{"a", "b"},
};
my_data = {
    std::vector<int>{1, 2},
    std::vector<std::string>{"a", "b"},
};
}
