#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
#include <variant>
int main() {
const auto my_data = std::map<std::string, std::variant<std::chrono::year_month_day, std::chrono::system_clock::time_point>>{
    {"date", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"datetime", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::chrono::year_month_day, std::chrono::system_clock::time_point>>{
    {"date", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"datetime", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
};
    (void)my_data;
    return 0;
}
