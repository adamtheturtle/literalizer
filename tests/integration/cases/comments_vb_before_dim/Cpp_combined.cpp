#include <initializer_list>
#include <string>
#include <map>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = {
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3000},
};
my_data = {
    // Configuration
    {"name", "app"},
    // Port setting
    {"port", 3000},
};
}
