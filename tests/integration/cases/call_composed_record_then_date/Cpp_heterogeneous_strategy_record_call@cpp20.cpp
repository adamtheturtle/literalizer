#include <chrono>
struct Record0 { int a{}; };
auto consume(auto...) { return 0; }
int main() {
auto item = Record0{
    .a = 1,
};
auto stamp = std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{2}, std::chrono::day{3}};
consume(stamp, item);
    return 0;
}
