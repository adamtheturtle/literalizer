#include <initializer_list>
#include <chrono>
struct Any {
    template<class T> Any(T&&) noexcept {}
    Any(std::initializer_list<Any>) noexcept {}
};
static void check_() {
Any my_data = {
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}},
};
my_data = {
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}},
    std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{6}, std::chrono::day{1}},
};
}
