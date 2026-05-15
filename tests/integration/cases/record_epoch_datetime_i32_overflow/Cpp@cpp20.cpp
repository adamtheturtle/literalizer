#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
int main() {
auto my_data = std::map<std::string, std::chrono::system_clock::time_point>{
    {"within_i32", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12}}},
    {"beyond_i32", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2099}, std::chrono::month{6}, std::chrono::day{15}}} + std::chrono::hours{8} + std::chrono::minutes{30}}},
};
    (void)my_data;
    return 0;
}
