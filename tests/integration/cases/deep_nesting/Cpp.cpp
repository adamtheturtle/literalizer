#include <initializer_list>
#include <string>
#include <map>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    {"level1", {{"level2", {{"level3", {{"level4", {{"value", "deep"}, {"items", std::vector<std::string>{"a", "b"}}}}}}, {"sibling", 42}}}, {"tags", {{{"name", "tag1"}, {"meta", {{"priority", 1}, {"labels", std::vector<std::string>{"x", "y"}}}}}}}}},
};
}
