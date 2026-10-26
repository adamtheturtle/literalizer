#include <chrono>
#include <initializer_list>
#include <map>
#include <string>
int main() {
auto my_data = {
    std::map<std::string, std::chrono::system_clock::time_point>{{"timestamp", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2040}, std::chrono::month{1}, std::chrono::day{1}}} + std::chrono::hours{3}}}},
    std::map<std::string, std::chrono::system_clock::time_point>{},
};
    (void)my_data;
    return 0;
}
