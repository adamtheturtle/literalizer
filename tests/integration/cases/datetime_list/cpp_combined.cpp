#include <chrono>
#include <initializer_list>
#include <cstddef>
#include <map>
#include <string>
#include <vector>
struct _Any {
    template<class T> _Any(T&&) noexcept {}
    _Any(std::initializer_list<_Any>) noexcept {}
};
void _check() {
_Any my_data = {
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{30}}} + std::chrono::hours{8},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{12}, std::chrono::day{25}}} + std::chrono::hours{18} + std::chrono::minutes{45},
};
my_data = {
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{30}}} + std::chrono::hours{8},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{12}, std::chrono::day{25}}} + std::chrono::hours{18} + std::chrono::minutes{45},
};
}
