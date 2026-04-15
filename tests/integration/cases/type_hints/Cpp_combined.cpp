#include <initializer_list>
#include <string>
#include <cstddef>
#include <chrono>
#include <map>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
void check_() {
auto my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
    {"joined", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"last_login", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
    {"avatar", "48656c6c6f"},
};
my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
    {"joined", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"last_login", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
    {"avatar", "48656c6c6f"},
};
}
