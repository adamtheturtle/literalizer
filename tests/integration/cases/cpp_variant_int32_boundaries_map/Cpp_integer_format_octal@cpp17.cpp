#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<long long, std::vector<int>>>{
    {"below", -020000000001LL},
    {"minimum", (-017777777777 - 1)},
    {"above", -017777777777},
    {"nested", std::vector<int>{0}},
};
    (void)my_data;
    return 0;
}
