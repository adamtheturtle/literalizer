#include <initializer_list>
#include <string>
#include <map>
int main() {
auto my_data = std::map<std::string, long long>{
    {"i32_below", -0b10000000000000000000000000000001LL},
    {"i32_minimum", -0b10000000000000000000000000000000LL},
    {"i32_above", -0b1111111111111111111111111111111},
    {"i32_maximum", 0b1111111111111111111111111111111},
    {"i32_over", 0b10000000000000000000000000000000},
    {"i64_minimum", (-9223372036854775807LL - 1)},
    {"i64_maximum", 0b111111111111111111111111111111111111111111111111111111111111111},
};
    (void)my_data;
    return 0;
}
