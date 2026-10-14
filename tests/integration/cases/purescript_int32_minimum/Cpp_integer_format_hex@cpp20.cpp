#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::vector<int>>>{
    {"minimum", (-0x7fffffff - 1)},
    {"neighbor", -0x7fffffff},
    {"maximum", 0x7fffffff},
    {"nested", std::vector<int>{(-0x7fffffff - 1)}},
};
    (void)my_data;
    return 0;
}
