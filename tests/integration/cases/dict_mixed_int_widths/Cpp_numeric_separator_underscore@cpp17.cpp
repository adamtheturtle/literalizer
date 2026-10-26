#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<long long, std::string>>{
    {"a", 1},
    {"b", 3'000'000'000},
    {"c", "x"},
};
    (void)my_data;
    return 0;
}
