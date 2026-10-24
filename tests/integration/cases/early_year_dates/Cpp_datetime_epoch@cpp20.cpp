#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
#include <variant>
int main() {
auto my_data = std::map<std::string, std::variant<std::chrono::year_month_day, long long>>{
    {"date", std::chrono::year_month_day{std::chrono::year{99}, std::chrono::month{5}, std::chrono::day{27}}},
    {"naive", -62135551800},
    {"recent", 1716804000},
};
    (void)my_data;
    return 0;
}
