#include <initializer_list>
#include <string>
#include <chrono>
#include <variant>
struct Record1 { int x{}; };
struct Record2 { std::chrono::year_month_day day; std::chrono::system_clock::time_point stamp; };
struct Record0 { Record1 plain; Record2 timed; };
int main() {
auto plain = Record1{
    .x = 1,
};
auto timed = Record2{
    .day = {std::chrono::year{2001}, std::chrono::month{1}, std::chrono::day{2}},
    .stamp = {std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{1}, std::chrono::day{2}}} + std::chrono::hours{3} + std::chrono::minutes{4} + std::chrono::seconds{5}},
};
auto my_data = Record0{
    .plain = plain,
    .timed = timed,
};
    (void)my_data;
    return 0;
}
