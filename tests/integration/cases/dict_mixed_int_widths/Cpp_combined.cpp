#include <initializer_list>
#include <string>
#include <map>
#include <variant>
int main() {
const auto my_data = std::map<std::string, std::variant<long long, std::string>>{
    {"a", 1},
    {"b", 3000000000},
    {"c", "x"},
};
(void)my_data;
my_data = std::map<std::string, std::variant<long long, std::string>>{
    {"a", 1},
    {"b", 3000000000},
    {"c", "x"},
};
    (void)my_data;
    return 0;
}
