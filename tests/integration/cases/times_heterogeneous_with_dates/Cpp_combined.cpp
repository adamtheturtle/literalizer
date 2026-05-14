#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
#include <vector>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<std::chrono::year_month_day, std::nullptr_t>>>{
    {"vals", std::vector<std::variant<std::chrono::year_month_day, std::nullptr_t>>{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}, "09:30:00"}},
};
(void)my_data;
my_data = std::map<std::string, std::vector<std::variant<std::chrono::year_month_day, std::nullptr_t>>>{
    {"vals", std::vector<std::variant<std::chrono::year_month_day, std::nullptr_t>>{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}, "09:30:00"}},
};
    (void)my_data;
    return 0;
}
