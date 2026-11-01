#include <chrono>
#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::map<std::string, std::vector<std::chrono::system_clock::time_point>>{
    {"stamps", std::vector<std::chrono::system_clock::time_point>{std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{2}, std::chrono::day{3}}} + std::chrono::hours{4} + std::chrono::minutes{5} + std::chrono::seconds{6}}, std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{2}, std::chrono::day{3}}} + std::chrono::hours{4} + std::chrono::minutes{5} + std::chrono::seconds{6}}, std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{2}, std::chrono::day{3}}} + std::chrono::hours{4} + std::chrono::minutes{5} + std::chrono::seconds{6}}, std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{2}, std::chrono::day{3}}} + std::chrono::hours{4} + std::chrono::minutes{5} + std::chrono::seconds{6}}, std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{2}, std::chrono::day{3}}} + std::chrono::hours{4} + std::chrono::minutes{5} + std::chrono::seconds{6}}, std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{2}, std::chrono::day{3}}} + std::chrono::hours{4} + std::chrono::minutes{5} + std::chrono::seconds{6}}}},
};
    (void)my_data;
    return 0;
}
