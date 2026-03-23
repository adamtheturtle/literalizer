#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
void _check() {
    [[maybe_unused]] _Any _v = {
    {"date", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"datetime", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
};
}
