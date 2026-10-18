#include <initializer_list>
#include <chrono>
#include <vector>
int main() {
auto my_data = std::vector<std::chrono::system_clock::time_point>{
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1970}, std::chrono::month{1}, std::chrono::day{1}}} + std::chrono::microseconds{1}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1969}, std::chrono::month{12}, std::chrono::day{31}}} + std::chrono::hours{23} + std::chrono::minutes{59} + std::chrono::seconds{59} + std::chrono::microseconds{500000}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1970}, std::chrono::month{1}, std::chrono::day{1}}} + std::chrono::seconds{1}},
};
    (void)my_data;
    return 0;
}
