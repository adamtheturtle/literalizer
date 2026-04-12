#include <initializer_list>
#include <string>
#include <map>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = std::vector<std::map<std::string, Any>>{
    {{"name", "Alice"}, {"age", 30}},
    {{"name", "Bob"}, {"age", 25}},
};
my_data = std::vector<std::map<std::string, Any>>{
    {{"name", "Alice"}, {"age", 30}},
    {{"name", "Bob"}, {"age", 25}},
};
}
