#include <initializer_list>
#include <chrono>
#include <vector>
void _check() {
    [[maybe_unused]] _Any _v = {
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{2}, std::chrono::day{20}},
};
}
