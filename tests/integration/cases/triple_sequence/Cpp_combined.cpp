#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = {
    1,
    "hello",
    true,
};
my_data = {
    1,
    "hello",
    true,
};
}
