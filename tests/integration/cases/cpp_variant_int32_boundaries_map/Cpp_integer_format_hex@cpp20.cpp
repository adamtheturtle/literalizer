#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<long long, std::vector<int>>>{
    {"below", -0x80000001LL},
    {"minimum", (-0x7fffffff - 1)},
    {"above", -0x7fffffff},
    {"nested", std::vector<int>{0x0}},
};
    (void)my_data;
    return 0;
}
