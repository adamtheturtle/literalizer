#include <initializer_list>
#include <string>
#include <chrono>
#include <map>
#include <vector>
#include <cstddef>
int main() {
auto my_data = std::vector<std::map<std::string, std::chrono::system_clock::time_point>>{
    std::map<std::string, std::chrono::system_clock::time_point>{{"timestamp", std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2020}, std::chrono::month{1}, std::chrono::day{1}}}}}},
    std::map<std::string, std::chrono::system_clock::time_point>{},
};
    (void)my_data;
    return 0;
}
