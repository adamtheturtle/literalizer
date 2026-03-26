#include <initializer_list>
#include <string>
#include <map>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = std::map<std::string, std::map<std::string, _Any>>{
    {"level1", {{"level2", {{"level3", std::map<std::string, std::map<std::string, _Any>>{{"level4", {{"value", "deep"}, {"items", std::vector<std::string>{"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", std::vector<std::map<std::string, _Any>>{{{"name", "tag1"}, {"meta", {{"priority", 1}, {"labels", std::vector<std::string>{"x", "y"}}}}}}}}},
};
}
