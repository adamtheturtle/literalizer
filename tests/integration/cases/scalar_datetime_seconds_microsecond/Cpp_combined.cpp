#include <chrono>
void _check() {
auto my_data = std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::seconds{45} + std::chrono::microseconds{123456};
my_data = std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::seconds{45} + std::chrono::microseconds{123456};
}
