#include <initializer_list>
#include <chrono>
int main() {
auto my_data = std::initializer_list<std::chrono::year_month_day>{
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}},
};
(void)my_data;
my_data = std::initializer_list<std::chrono::year_month_day>{
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}},
};
    (void)my_data;
    return 0;
}
