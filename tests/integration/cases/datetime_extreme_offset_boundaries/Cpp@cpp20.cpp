#include <chrono>
#include <vector>
int main() {
auto my_data = std::vector<std::chrono::system_clock::time_point>{
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{6}, std::chrono::day{15}}} + std::chrono::hours{12}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{6}, std::chrono::day{15}}} + std::chrono::hours{12}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{6}, std::chrono::day{15}}} + std::chrono::hours{12}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{6}, std::chrono::day{15}}} + std::chrono::hours{12}},
};
    (void)my_data;
    return 0;
}
