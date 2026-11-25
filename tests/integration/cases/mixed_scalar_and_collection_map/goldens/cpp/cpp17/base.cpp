#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::string, std::vector<int>, std::map<std::string, std::string>>>{
    {"a", 1},
    {"b", "x"},
    {"e", std::vector<int>{1, 2}},
    {"f", std::map<std::string, std::string>{{"g", "h"}}},
};
    (void)my_data;
    return 0;
}
