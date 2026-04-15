#include <initializer_list>
#include <string>
#include <map>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::map<std::string, double>{
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
my_data = std::map<std::string, double>{
    {"a", 1},
    {"b", 2.5},
    {"c", 3},
};
}
