#include <initializer_list>
#include <string>
#include <chrono>
#include <cmath>
#include <vector>
#include <variant>
auto capture(auto...) { return 0; }
int main() {
capture(static_cast<double>(NAN), static_cast<double>(INFINITY), -static_cast<double>(INFINITY), 1.25, "2024-01-15", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{34} + std::chrono::seconds{56}}, "[ordinary text]");
    return 0;
}
