#include <initializer_list>
#include <cstddef>
#include <map>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    {"level1", {{"level2", {{"level3", {{"level4", {{"value", "deep"}, {"items", std::vector<std::string>{"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", {{{"name", "tag1"}, {"meta", {{"priority", 1}, {"labels", std::vector<std::string>{"x", "y"}}}}}}}}},
};
}
