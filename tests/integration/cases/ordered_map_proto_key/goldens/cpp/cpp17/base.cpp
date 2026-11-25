#include <map>
#include <string>
#include <utility>
#include <variant>
#include <vector>
int main() {
auto my_data = std::vector<std::pair<std::string, std::variant<std::map<std::string, int>, int>>>{
    {"__proto__", std::map<std::string, int>{{"x", 1}}},
    {"ordinary", 2},
};
    (void)my_data;
    return 0;
}
