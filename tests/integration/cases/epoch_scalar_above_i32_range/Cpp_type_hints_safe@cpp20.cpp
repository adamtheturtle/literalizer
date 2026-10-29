#include <chrono>
int main() {
auto my_data = std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2099}, std::chrono::month{6}, std::chrono::day{15}}} + std::chrono::hours{8} + std::chrono::minutes{30}};
    (void)my_data;
    return 0;
}
