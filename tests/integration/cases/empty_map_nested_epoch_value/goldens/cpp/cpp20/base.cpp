#include <chrono>
#include <map>
#include <string>
#include <vector>
int main() {
auto my_data = std::vector<std::map<std::string, std::map<std::string, std::vector<std::chrono::system_clock::time_point>>>>{
    std::map<std::string, std::map<std::string, std::vector<std::chrono::system_clock::time_point>>>{{"nested", std::map<std::string, std::vector<std::chrono::system_clock::time_point>>{{"times", std::vector<std::chrono::system_clock::time_point>{std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1900}, std::chrono::month{1}, std::chrono::day{1}}}}}}}}},
    std::map<std::string, std::map<std::string, std::vector<std::chrono::system_clock::time_point>>>{},
};
    (void)my_data;
    return 0;
}
