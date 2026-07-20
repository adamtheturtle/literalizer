#include <initializer_list>
#include <string>
#include <cstddef>
#include <chrono>
#include <map>
#include <variant>
struct Record0 { std::string s; int i{}; double f{}; bool b{}; std::nullptr_t n{}; std::chrono::year_month_day d; std::chrono::system_clock::time_point dt; std::string by; };
int main() {
auto my_data = Record0{
    .s = "string",
    .i = 1,
    .f = 1.5,
    .b = true,
    .n = nullptr,
    .d = std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    .dt = std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12}},
    .by = "48656c6c6f",
};
    (void)my_data;
    return 0;
}
