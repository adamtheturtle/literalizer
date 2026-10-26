#include <chrono>
auto process(auto...) { return 0; }
auto emit(auto...) { return 0; }
int main() {
emit(process(1), std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}});
    return 0;
}
