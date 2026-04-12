#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = std::vector<std::map<std::string, Any>>{
    {{"name", "Alice"}, {"age", 30}},
    {{"name", "Bob"}, {"age", 25}},
};
}
