#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<long long, std::vector<int>>>{
    {"below", -0b10000000000000000000000000000001LL},
    {"minimum", (-0b1111111111111111111111111111111 - 1)},
    {"above", -0b1111111111111111111111111111111},
    {"nested", std::vector<int>{0b0}},
};
    (void)my_data;
    return 0;
}
