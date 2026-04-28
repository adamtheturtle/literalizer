#include <initializer_list>
#include <chrono>
int main() {
auto my_data = std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{18};
    (void)my_data;
    return 0;
}
