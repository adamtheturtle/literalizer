#include <initializer_list>
#include <string>
#include <map>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = {
    {"name", "Alice"},
    {"tags", {true, 42, "apple"}},
};
my_data = {
    {"name", "Alice"},
    {"tags", {true, 42, "apple"}},
};
}
