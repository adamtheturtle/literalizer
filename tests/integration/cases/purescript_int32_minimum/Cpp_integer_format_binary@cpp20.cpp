#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::vector<int>>>{
    {"minimum", -0b10000000000000000000000000000000LL},
    {"neighbor", -0b1111111111111111111111111111111},
    {"maximum", 0b1111111111111111111111111111111},
    {"nested", std::vector<int>{-0b10000000000000000000000000000000LL}},
};
    (void)my_data;
    return 0;
}
