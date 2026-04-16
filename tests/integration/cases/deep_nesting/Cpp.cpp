#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = std::map<std::string, std::map<std::string, Any>>{
    {"level1", {{"level2", {{"level3", std::map<std::string, std::map<std::string, Any>>{{"level4", {{"value", "deep"}, {"items", std::vector<std::string>{"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", std::vector<std::map<std::string, Any>>{{{"name", "tag1"}, {"meta", {{"priority", 1}, {"labels", std::vector<std::string>{"x", "y"}}}}}}}}},
};
}
