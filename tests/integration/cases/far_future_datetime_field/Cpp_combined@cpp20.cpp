#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
int main() {
auto my_data = std::map<std::string, std::chrono::system_clock::time_point>{
    {"ts", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{3000}, std::chrono::month{12}, std::chrono::day{31}}} + std::chrono::hours{23} + std::chrono::minutes{59} + std::chrono::seconds{59} + std::chrono::microseconds{999999}}},
};
(void)my_data;
my_data = std::map<std::string, std::chrono::system_clock::time_point>{
    {"ts", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{3000}, std::chrono::month{12}, std::chrono::day{31}}} + std::chrono::hours{23} + std::chrono::minutes{59} + std::chrono::seconds{59} + std::chrono::microseconds{999999}}},
};
    (void)my_data;
    return 0;
}
