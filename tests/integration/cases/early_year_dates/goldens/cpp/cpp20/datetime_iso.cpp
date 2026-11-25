#include <chrono>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::chrono::year_month_day, std::string>>{
    {"date", std::chrono::year_month_day{std::chrono::year{99}, std::chrono::month{5}, std::chrono::day{27}}},
    {"naive", "0001-01-01T12:30:00"},
    {"recent", "2024-05-27T10:00:00"},
};
    (void)my_data;
    return 0;
}
