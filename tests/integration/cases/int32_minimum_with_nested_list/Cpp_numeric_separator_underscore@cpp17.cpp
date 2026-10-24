#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::vector<int>>>{
    {"minimum", (-2'147'483'647 - 1)},
    {"neighbor", -2'147'483'647},
    {"maximum", 2'147'483'647},
    {"nested", std::vector<int>{(-2'147'483'647 - 1)}},
};
    (void)my_data;
    return 0;
}
