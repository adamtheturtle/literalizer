#include <initializer_list>
#include <chrono>
int main() {
const auto my_data = std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}};
(void)my_data;
my_data = std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}};
    (void)my_data;
    return 0;
}
