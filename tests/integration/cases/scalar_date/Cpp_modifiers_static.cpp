#include <initializer_list>
#include <chrono>
void check_() {
static auto my_data = std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}};
}
