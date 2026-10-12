#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::vector<int>>>{
    {"minimum", -020000000000LL},
    {"neighbor", -017777777777},
    {"maximum", 017777777777},
    {"nested", std::vector<int>{-020000000000LL}},
};
    (void)my_data;
    return 0;
}
