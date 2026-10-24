#include <initializer_list>
#include <chrono>
#include <vector>
int main() {
auto my_data = std::vector<std::chrono::system_clock::time_point>{
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1901}, std::chrono::month{12}, std::chrono::day{13}}} + std::chrono::hours{20} + std::chrono::minutes{45} + std::chrono::seconds{51}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1901}, std::chrono::month{12}, std::chrono::day{13}}} + std::chrono::hours{20} + std::chrono::minutes{45} + std::chrono::seconds{52}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2038}, std::chrono::month{1}, std::chrono::day{19}}} + std::chrono::hours{3} + std::chrono::minutes{14} + std::chrono::seconds{7}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2038}, std::chrono::month{1}, std::chrono::day{19}}} + std::chrono::hours{3} + std::chrono::minutes{14} + std::chrono::seconds{8}},
};
    (void)my_data;
    return 0;
}
