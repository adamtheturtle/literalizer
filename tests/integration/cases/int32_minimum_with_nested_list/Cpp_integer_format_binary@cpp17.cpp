#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::vector<int>>>{
    {"minimum", (-0b1111111111111111111111111111111 - 1)},
    {"neighbor", -0b1111111111111111111111111111111},
    {"maximum", 0b1111111111111111111111111111111},
    {"nested", std::vector<int>{(-0b1111111111111111111111111111111 - 1)}},
};
    (void)my_data;
    return 0;
}
