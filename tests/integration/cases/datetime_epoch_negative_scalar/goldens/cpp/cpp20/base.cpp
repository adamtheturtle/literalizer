#include <chrono>
int main() {
auto my_data = std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1969}, std::chrono::month{12}, std::chrono::day{31}}} + std::chrono::hours{23} + std::chrono::minutes{59} + std::chrono::seconds{59}};
    (void)my_data;
    return 0;
}
