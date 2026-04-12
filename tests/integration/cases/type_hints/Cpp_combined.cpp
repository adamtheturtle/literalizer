#include <initializer_list>
#include <string>
#include <cstddef>
#include <chrono>
#include <map>
namespace {
struct Any {
    template<class T> Any(T&& /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions,bugprone-forwarding-reference-overload)
    Any(std::initializer_list<Any> /*unused*/) noexcept {}  // NOLINT(google-explicit-constructor,hicpp-explicit-conversions)
};
}  // namespace
static void check_() {
Any my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
    {"joined", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"last_login", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
    {"avatar", "48656c6c6f"},
};
my_data = {
    {"name", "Alice"},
    {"age", 30},
    {"active", true},
    {"score", nullptr},
    {"joined", std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}},
    {"last_login", std::chrono::sys_days{std::chrono::year_month_day{std::chrono::year{2024}, std::chrono::month{1}, std::chrono::day{15}}} + std::chrono::hours{12} + std::chrono::minutes{30}},
    {"avatar", "48656c6c6f"},
};
}
