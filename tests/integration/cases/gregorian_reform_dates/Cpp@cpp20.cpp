#include <chrono>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::chrono::year_month_day, std::chrono::system_clock::time_point>>{
    {"ancient_date", std::chrono::year_month_day{std::chrono::year{1500}, std::chrono::month{3}, std::chrono::day{1}}},
    {"modern_date", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"before_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{4}}},
    {"gap_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{10}}},
    {"transition_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{15}}},
    {"after_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{16}}},
    {"before_naive", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{4}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::microseconds{1}}},
    {"gap_naive", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{10}}} + std::chrono::hours{12} + std::chrono::minutes{30} + std::chrono::microseconds{500000}}},
    {"transition_positive", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{15}}} + std::chrono::minutes{30}}},
    {"transition_negative", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{15}}} + std::chrono::hours{23} + std::chrono::minutes{30}}},
    {"after_positive", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{16}}} + std::chrono::minutes{30}}},
};
    (void)my_data;
    return 0;
}
