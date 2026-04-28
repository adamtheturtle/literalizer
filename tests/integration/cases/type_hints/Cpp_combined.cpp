#include <initializer_list>
#include <string>
#include <cstddef>
#include <chrono>
#include <map>
#include <variant>
auto main() -> int {
auto my_data = std::map<std::string, std::variant<std::string, int, bool, std::nullptr_t, std::chrono::year_month_day, std::chrono::system_clock::time_point>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
    {"joined", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"last_login", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
    {"avatar", "48656c6c6f"},
};
(void)my_data;
my_data = std::map<std::string, std::variant<std::string, int, bool, std::nullptr_t, std::chrono::year_month_day, std::chrono::system_clock::time_point>>{
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
    {"joined", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"last_login", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
    {"avatar", "48656c6c6f"},
};
    (void)my_data;
    return 0;
}
