#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = std::vector<std::map<std::string, double>>{
    std::map<std::string, double>{{"x", 1}, {"y", 2.5}},
    std::map<std::string, double>{{"x", 3}, {"y", 4.0}},
};
my_data = std::vector<std::map<std::string, double>>{
    std::map<std::string, double>{{"x", 1}, {"y", 2.5}},
    std::map<std::string, double>{{"x", 3}, {"y", 4.0}},
};
}
