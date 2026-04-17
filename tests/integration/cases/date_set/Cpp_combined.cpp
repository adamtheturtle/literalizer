#include <initializer_list>
#include <chrono>
void check_() {
auto my_data = std::initializer_list<std::chrono::year_month_day>{
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}},
};
my_data = std::initializer_list<std::chrono::year_month_day>{
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}},
};
}
