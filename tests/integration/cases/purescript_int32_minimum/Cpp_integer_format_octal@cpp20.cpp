#include <initializer_list>
#include <string>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<int, std::vector<int>>>{
    {"minimum", (-017777777777 - 1)},
    {"neighbor", -017777777777},
    {"maximum", 017777777777},
    {"nested", std::vector<int>{(-017777777777 - 1)}},
};
    (void)my_data;
    return 0;
}
