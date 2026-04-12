#include <initializer_list>
#include <string>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = {
    "apple",
    "banana",
    "cherry",
};
my_data = {
    "apple",
    "banana",
    "cherry",
};
}
