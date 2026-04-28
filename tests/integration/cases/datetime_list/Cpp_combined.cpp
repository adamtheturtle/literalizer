#include <initializer_list>
#include <chrono>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::chrono::system_clock::time_point>{
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::microseconds{123456},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}}} + std::chrono::hours{8},
};
(void)my_data;
my_data = std::vector<std::chrono::system_clock::time_point>{
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::microseconds{123456},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}}} + std::chrono::hours{8},
};
    (void)my_data;
    return 0;
}
