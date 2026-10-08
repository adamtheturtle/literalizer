#include <initializer_list>
#include <string>
#include <cstddef>
#include <unordered_map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::unordered_map<std::string, std::variant<std::string, bool, int, double, std::nullptr_t, std::vector<int>, std::unordered_map<std::string, int>>>>{
    std::unordered_map<std::string, std::variant<std::string, bool, int, double, std::nullptr_t, std::vector<int>, std::unordered_map<std::string, int>>>{{"name", "Ada"}, {"active", true}, {"count", 1}, {"score", 1.5}, {"missing", nullptr}, {"scores", std::vector<int>{1, 2}}, {"child", std::unordered_map<std::string, int>{{"age", 3}}}},
    std::unordered_map<std::string, std::variant<std::string, bool, int, double, std::nullptr_t, std::vector<int>, std::unordered_map<std::string, int>>>{{"name", "Bob"}, {"active", false}, {"count", 2}, {"score", 2.5}, {"missing", nullptr}, {"scores", std::vector<int>{4}}, {"child", std::unordered_map<std::string, int>{{"age", 5}}}},
};
    (void)my_data;
    return 0;
}
