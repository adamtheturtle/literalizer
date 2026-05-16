#include <initializer_list>
#include <string>
#include <cstddef>
#include <chrono>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::string, int, double, bool, std::nullptr_t, std::chrono::year_month_day, long long>>{
    {"s", "string"},
    {"i", 1},
    {"f", 1.5},
    {"b", true},
    {"n", nullptr},
    {"d", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"dt", 1705320000},
    {"by", "48656c6c6f"},
};
    (void)my_data;
    return 0;
}
