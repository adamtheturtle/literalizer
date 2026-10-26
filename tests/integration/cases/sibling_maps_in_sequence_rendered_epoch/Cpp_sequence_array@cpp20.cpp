#include <chrono>
#include <initializer_list>
#include <map>
#include <string>
#include <variant>
int main() {
auto my_data = {
    std::map<std::string, std::variant<std::chrono::system_clock::time_point, int>>{{"k", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2040}, std::chrono::month{1}, std::chrono::day{1}}}}}},
    std::map<std::string, std::variant<std::chrono::system_clock::time_point, int>>{{"k", 1}},
};
    (void)my_data;
    return 0;
}
