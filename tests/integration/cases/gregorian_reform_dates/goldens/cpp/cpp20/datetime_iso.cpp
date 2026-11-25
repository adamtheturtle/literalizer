#include <chrono>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::chrono::year_month_day, std::string>>{
    {"ancient_date", std::chrono::year_month_day{std::chrono::year{1500}, std::chrono::month{3}, std::chrono::day{1}}},
    {"modern_date", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"before_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{4}}},
    {"gap_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{10}}},
    {"transition_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{15}}},
    {"after_date", std::chrono::year_month_day{std::chrono::year{1582}, std::chrono::month{10}, std::chrono::day{16}}},
    {"before_naive", "1582-10-04T12:30:00.000001"},
    {"gap_naive", "1582-10-10T12:30:00.500000"},
    {"transition_positive", "1582-10-15T00:30:00+18:00"},
    {"transition_negative", "1582-10-15T23:30:00-18:00"},
    {"after_positive", "1582-10-16T00:30:00+18:00"},
};
    (void)my_data;
    return 0;
}
