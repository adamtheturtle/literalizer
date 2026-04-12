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
    {"scores", std::map<std::string, std::string>{{"1", "first"}, {"2", "second"}}},
};
}
