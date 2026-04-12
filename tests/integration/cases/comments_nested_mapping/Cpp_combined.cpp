#include <initializer_list>
#include <string>
#include <map>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = {
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
my_data = {
    {"a", std::map<std::string, int>{{"x", 1}}},
    {"b", 2},
};
}
