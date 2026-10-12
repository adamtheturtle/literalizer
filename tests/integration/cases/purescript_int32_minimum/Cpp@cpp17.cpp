#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::vector<int>>>{
    {"minimum", -2147483648},
    {"neighbor", -2147483647},
    {"maximum", 2147483647},
    {"nested", std::vector<int>{-2147483648}},
};
    (void)my_data;
    return 0;
}
