#include <chrono>
#include <string>
struct Record0 { std::chrono::year_month_day birthday; std::chrono::system_clock::time_point moment; std::string at; };
int main() {
auto my_data = Record0{
    .birthday = {std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    .moment = {std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
    .at = "09:30:00",
};
    (void)my_data;
    return 0;
}
