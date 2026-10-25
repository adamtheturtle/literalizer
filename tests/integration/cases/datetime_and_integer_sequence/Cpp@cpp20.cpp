#include <initializer_list>
#include <chrono>
#include <vector>
#include <variant>
int main() {
auto my_data = std::vector<std::variant<std::chrono::system_clock::time_point, int>>{
    std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2000}, std::chrono::month{1}, std::chrono::day{1}}} + std::chrono::hours{1} + std::chrono::minutes{2} + std::chrono::seconds{3}},
    1,
};
    (void)my_data;
    return 0;
}
