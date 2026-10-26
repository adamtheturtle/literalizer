#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<long long, std::vector<int>>>{
    {"below", -2147483649},
    {"minimum", (-2147483647 - 1)},
    {"above", -2147483647},
    {"nested", std::vector<int>{0}},
};
    (void)my_data;
    return 0;
}
