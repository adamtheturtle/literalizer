#include <chrono>
int main() {
auto my_data = std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1901}, std::chrono::month{12}, std::chrono::day{13}}} + std::chrono::hours{20} + std::chrono::minutes{45} + std::chrono::seconds{51}};
    (void)my_data;
    return 0;
}
