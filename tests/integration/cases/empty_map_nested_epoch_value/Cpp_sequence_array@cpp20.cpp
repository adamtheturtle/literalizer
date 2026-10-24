#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
#include <array>
#include <cstddef>
#include <variant>
int main() {
auto my_data = {
    std::map<std::string, std::map<std::string, std::array<std::chrono::system_clock::time_point, 1>>>{{"nested", std::map<std::string, std::array<std::chrono::system_clock::time_point, 1>>{{"times", std::array<std::chrono::system_clock::time_point, 1>{std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1900}, std::chrono::month{1}, std::chrono::day{1}}}}}}}}},
    std::map<std::string, std::map<std::string, std::array<std::chrono::system_clock::time_point, 1>>>{},
};
    (void)my_data;
    return 0;
}
