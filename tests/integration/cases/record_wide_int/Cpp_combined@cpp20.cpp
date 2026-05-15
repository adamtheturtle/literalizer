#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<long long, double, std::string, bool>>{
    {"quantity", 1000000},
    {"big", 18446744073709551615ULL},
    {"ratio", 2.5},
    {"label", "tag"},
    {"ok", true},
};
(void)my_data;
my_data = std::map<std::string, std::variant<long long, double, std::string, bool>>{
    {"quantity", 1000000},
    {"big", 18446744073709551615ULL},
    {"ratio", 2.5},
    {"label", "tag"},
    {"ok", true},
};
    (void)my_data;
    return 0;
}
