#include <initializer_list>
#include <chrono>
#include <vector>
#include <variant>
auto check(auto...) { return 0; }
int main() {
check(std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{10} + std::chrono::minutes{30}}, std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}});
    return 0;
}
