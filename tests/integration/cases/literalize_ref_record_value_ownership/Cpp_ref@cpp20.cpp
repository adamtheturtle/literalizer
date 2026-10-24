#include <initializer_list>
#include <string>
#include <cstddef>
#include <chrono>
#include <variant>
struct Record1 { int integer{}; bool boolean{}; double decimal{}; std::nullptr_t null{}; };
struct Record3 { int integer{}; };
struct Record2 { Record3 child; };
struct Record4 { std::string text; };
struct Record5 { std::chrono::year_month_day day; std::chrono::system_clock::time_point stamp; };
struct Record0 { Record1 trivial; Record2 nested; Record4 owning; Record5 calendar; };
int main() {
auto trivial = Record1{
    .integer = 1,
    .boolean = true,
    .decimal = 1.5,
    .null = nullptr,
};
auto nested = Record2{
    .child = {
        .integer = 2,
    },
};
auto owning = Record4{
    .text = "owned",
};
auto calendar = Record5{
    .day = {std::chrono::year{2001}, std::chrono::month{1}, std::chrono::day{2}},
    .stamp = {std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2001}, std::chrono::month{1}, std::chrono::day{2}}} + std::chrono::hours{3} + std::chrono::minutes{4} + std::chrono::seconds{5}},
};
auto my_data = Record0{
    .trivial = trivial,
    .nested = nested,
    .owning = std::move(owning),
    .calendar = calendar,
};
    (void)my_data;
    return 0;
}
