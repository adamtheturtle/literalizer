#include <initializer_list>
#include <string>
#include <chrono>
#include <unordered_map>
#include <variant>
int main() {
auto my_data = std::unordered_map<std::string, std::variant<std::chrono::year_month_day, std::string, std::chrono::system_clock::time_point>>{
    {"birthday", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"meeting", "09:30:00"},
    {"event_time", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}}},
};
    (void)my_data;
    return 0;
}
