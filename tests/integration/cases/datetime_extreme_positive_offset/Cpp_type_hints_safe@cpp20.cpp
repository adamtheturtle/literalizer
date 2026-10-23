#include <initializer_list>
#include <chrono>
int main() {
auto my_data = std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{6}, std::chrono::day{15}}} + std::chrono::hours{12}};
    (void)my_data;
    return 0;
}
