#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
int main() {
auto my_data = std::map<std::string, std::chrono::system_clock::time_point>{
    {"half", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1979}, std::chrono::month{5}, std::chrono::day{27}}} + std::chrono::hours{7} + std::chrono::minutes{32} + std::chrono::microseconds{500000}}},
    {"milli", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1979}, std::chrono::month{5}, std::chrono::day{27}}} + std::chrono::hours{7} + std::chrono::minutes{32} + std::chrono::microseconds{100000}}},
    {"max_milli", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1979}, std::chrono::month{5}, std::chrono::day{27}}} + std::chrono::hours{7} + std::chrono::minutes{32} + std::chrono::microseconds{999000}}},
    {"whole", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1979}, std::chrono::month{5}, std::chrono::day{27}}} + std::chrono::hours{7} + std::chrono::minutes{32}}},
};
    (void)my_data;
    return 0;
}
