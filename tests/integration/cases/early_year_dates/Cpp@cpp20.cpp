#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::chrono::year_month_day, std::chrono::system_clock::time_point>>{
    {"date", std::chrono::year_month_day{std::chrono::year{99}, std::chrono::month{5}, std::chrono::day{27}}},
    {"naive", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1}, std::chrono::month{1}, std::chrono::day{1}}} + std::chrono::hours{12} + std::chrono::minutes{30}}},
    {"recent", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{5}, std::chrono::day{27}}} + std::chrono::hours{10}}},
};
    (void)my_data;
    return 0;
}
