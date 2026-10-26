#include <chrono>
#include <string>
struct Record0 { std::chrono::year_month_day event_date; std::string event_time; std::chrono::system_clock::time_point event_datetime; };
int main() {
auto my_data = Record0{
    .event_date = {std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    .event_time = "12:30:00",
    .event_datetime = {std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
};
    (void)my_data;
    return 0;
}
