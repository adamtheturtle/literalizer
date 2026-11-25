#include <map>
#include <string>
#include <variant>
#include <vector>
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
