#include <initializer_list>
#include <chrono>
#include <vector>
auto main() -> int {
auto my_data = std::vector<std::chrono::year_month_day>{
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{2}, std::chrono::day{20}},
};
(void)my_data;
my_data = std::vector<std::chrono::year_month_day>{
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{2}, std::chrono::day{20}},
};
    (void)my_data;
    return 0;
}
