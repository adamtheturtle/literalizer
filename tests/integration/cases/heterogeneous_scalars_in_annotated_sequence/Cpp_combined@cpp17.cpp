#include <initializer_list>
#include <cstddef>
#include <chrono>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<bool, double, std::nullptr_t, std::chrono::year_month_day, std::chrono::system_clock::time_point, std::vector<std::nullptr_t>>>{
    true,
    1.5,
    nullptr,
    std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{1}, std::chrono::day{1}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{1}, std::chrono::day{1}}}},
    std::vector<std::nullptr_t>{},
};
(void)my_data;
my_data = std::vector<std::variant<bool, double, std::nullptr_t, std::chrono::year_month_day, std::chrono::system_clock::time_point, std::vector<std::nullptr_t>>>{
    true,
    1.5,
    nullptr,
    std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{1}, std::chrono::day{1}},
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{1}, std::chrono::day{1}}}},
    std::vector<std::nullptr_t>{},
};
    (void)my_data;
    return 0;
}
