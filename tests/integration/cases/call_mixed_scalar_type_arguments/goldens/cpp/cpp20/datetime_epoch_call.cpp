#include <cmath>
#include <chrono>
auto capture(auto...) { return 0; }
int main() {
capture(static_cast<double>(NAN), static_cast<double>(INFINITY), -static_cast<double>(INFINITY), 1.25, std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}, 1705322096, "[ordinary text]");
    return 0;
}
