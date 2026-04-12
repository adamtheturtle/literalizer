#include <initializer_list>
#include <chrono>
#include <vector>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}
    Any(std::initializer_list<Any> /*unused*/) noexcept {}
};
}  // namespace
static void check_() {
Any my_data = {
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::microseconds{123456},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}}} + std::chrono::hours{8},
};
my_data = {
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::microseconds{123456},
    std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}}} + std::chrono::hours{8},
};
}
