#include <initializer_list>
#include <string>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
Any my_data = {
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
my_data = {
    42,
    3.14,
    true,
    false,
    "hello \"world\"",
};
}
