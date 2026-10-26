#include <chrono>
#include <map>
#include <string>
#include <variant>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::variant<std::chrono::year_month_day, std::string>>>{
    {"vals", std::vector<std::variant<std::chrono::year_month_day, std::string>>{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}, "09:30:00"}},
};
(void)my_data;
my_data = std::map<std::string, std::vector<std::variant<std::chrono::year_month_day, std::string>>>{
    {"vals", std::vector<std::variant<std::chrono::year_month_day, std::string>>{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}, "09:30:00"}},
};
    (void)my_data;
    return 0;
}
