#include <initializer_list>
#include <chrono>
#include <vector>
int main() {
auto my_data = std::vector<std::chrono::system_clock::time_point>{
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{1960}, std::chrono::month{1}, std::chrono::day{1}}}},
};
    (void)my_data;
    return 0;
}
