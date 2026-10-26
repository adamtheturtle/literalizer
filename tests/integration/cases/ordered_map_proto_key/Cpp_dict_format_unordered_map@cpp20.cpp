#include <string>
#include <unordered_map>
#include <utility>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::variant<std::unordered_map<std::string, int>, int>>>{
    {"__proto__", std::unordered_map<std::string, int>{{"x", 1}}},
    {"ordinary", 2},
};
    (void)my_data;
    return 0;
}
