#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::variant<long, std::vector<long>>>{
    {"below", -2147483649L},
    {"minimum", -2147483648L},
    {"above", -2147483647L},
    {"nested", std::vector<long>{0L}},
};
    (void)my_data;
    return 0;
}
