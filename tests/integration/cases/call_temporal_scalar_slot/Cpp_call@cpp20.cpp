#include <initializer_list>
#include <chrono>
#include <vector>
#include <variant>
auto process(auto...) { return 0; }
int main() {
process("09:30:00");
process(std::chrono::system_clock::time_point{std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}}});
process(1);
    return 0;
}
