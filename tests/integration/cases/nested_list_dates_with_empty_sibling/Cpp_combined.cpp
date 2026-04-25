#include <initializer_list>
#include <chrono>
#include <vector>
#include <cstddef>
void check_() {
auto my_data = std::vector<std::vector<std::chrono::year_month_day>>{
    std::vector<std::chrono::year_month_day>{std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{1}, std::chrono::day{1}}, std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{1}, std::chrono::day{2}}},
    std::vector<std::chrono::year_month_day>{},
    std::vector<std::chrono::year_month_day>{std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{2}, std::chrono::day{3}}, std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{2}, std::chrono::day{4}}},
};
(void)my_data;
my_data = std::vector<std::vector<std::chrono::year_month_day>>{
    std::vector<std::chrono::year_month_day>{std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{1}, std::chrono::day{1}}, std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{1}, std::chrono::day{2}}},
    std::vector<std::chrono::year_month_day>{},
    std::vector<std::chrono::year_month_day>{std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{2}, std::chrono::day{3}}, std::chrono::year_month_day{std::chrono::year{2026}, std::chrono::month{2}, std::chrono::day{4}}},
};
    (void)my_data;
}
